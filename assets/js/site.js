(function () {
  var body = document.body;
  var header = document.querySelector('.header');

  /* Header height -> first section offset */
  function setHeaderHeight() {
    if (header) document.documentElement.style.setProperty('--header-h', header.offsetHeight + 'px');
  }

  /* Mobile menu */
  var burger = document.querySelector('.header-burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = body.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('.mobile-menu a').forEach(function (a) {
      a.addEventListener('click', function () { body.classList.remove('menu-open'); });
    });
  }

  /* Scaled text: fit the heading to the width of its block */
  function fitText() {
    document.querySelectorAll('.scaled-text').forEach(function (el) {
      var box = el.parentElement;
      el.style.fontSize = '100px';
      var w = el.scrollWidth;
      if (w > 0) el.style.fontSize = (100 * box.clientWidth / w) + 'px';
    });
  }

  /* Accordion */
  document.querySelectorAll('.accordion-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var li = btn.closest('li');
      var open = li.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  /* Carousel (infinite loop, one item per click) */
  document.querySelectorAll('.carousel').forEach(function (car) {
    var track = car.querySelector('.carousel-track');
    var items = Array.prototype.slice.call(track.children);
    var n = items.length;
    if (!n) return;
    // clone for looping
    items.forEach(function (it) { track.appendChild(it.cloneNode(true)); });
    items.slice().reverse().forEach(function (it) { track.insertBefore(it.cloneNode(true), track.firstChild); });
    var index = n;
    function per() { return parseFloat(getComputedStyle(car).getPropertyValue('--per')) || 4; }
    function position() {
      var w = car.querySelector('.carousel-viewport').clientWidth;
      var style = getComputedStyle(car.querySelector('.carousel-viewport'));
      var inner = w - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
      return inner / per();
    }
    function apply(animate) {
      track.style.transition = animate ? '' : 'none';
      track.style.transform = 'translateX(' + (-index * position()) + 'px)';
    }
    function placeArrows() {
      var img = car.querySelector('.carousel-item .media');
      if (!img) return;
      var top = img.offsetTop + img.offsetHeight / 2 - 30;
      car.querySelectorAll(':scope > .carousel-arrow').forEach(function (a) { a.style.top = top + 'px'; });
    }
    track.addEventListener('transitionend', function () {
      if (index >= 2 * n) { index -= n; apply(false); }
      if (index < n) { index += n; apply(false); }
    });
    car.querySelectorAll('.prev').forEach(function (b) { b.addEventListener('click', function () { index--; apply(true); }); });
    car.querySelectorAll('.next').forEach(function (b) { b.addEventListener('click', function () { index++; apply(true); }); });
    window.addEventListener('resize', function () { apply(false); placeArrows(); });
    window.addEventListener('load', placeArrows);
    apply(false); placeArrows();
  });

  function onResize() { setHeaderHeight(); fitText(); }
  window.addEventListener('resize', onResize);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(onResize);
  window.addEventListener('load', onResize);
  onResize();
})();
