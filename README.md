# Santa Cruz Nursery & Farm: static site

A hand-built static copy of [santacruznursery.com](https://www.santacruznursery.com) (Squarespace 7.1), with no Squarespace runtime.

The layout follows Squarespace's own rules, measured from the live site:

- **Fluid-engine grid:** 8 columns on mobile and 24 columns at 768px and wider. Every block uses the live site's grid areas for both breakpoints.
- **Type scale:** headings and body text use the same fluid sizes and line-heights as the live site. Below 768px sizes scale with `min(1vh, 9px)`. At 768px and wider they scale with `vw` and are capped at the rem values.
- **Section spacing:** padding uses `max(1vw, min(1vh, 9px))` and min-heights are in `vh`, the same as the live site.
- **Colors:** the white, black, dark and black-bold section themes match the live site's color tokens.
- **Interactive pieces:** transparent fixed header, mobile menu, accordions, plant-page carousels, the Vimeo embeds and the contact map.

## Structure

```
build.py            generator: all page content and layout data lives here
assets/css/site.css all styles
assets/js/site.js   menu, accordion, carousel, scaled "Our Story" heading
index.html …        generated pages (one folder per URL, same slugs as the live site)
```

To change content, edit `build.py` and run:

```bash
python3 build.py                 # for https://<user>.github.io/SN_Site/
BASE_PATH=/ python3 build.py     # when serving from a custom domain root
```

`BASE_PATH` only affects `404.html`. Every other page uses relative links, so the site works from any folder.

## Fonts

The live site uses Adobe Fonts (Freight Text Pro, Adobe Caslon Pro, Freight Sans Pro) through Squarespace's license. Squarespace's font kit only loads on Squarespace domains. Until you add your own kit, the pages use similar Google Fonts (Crimson Pro, Libre Caslon Text, Source Sans 3).

To get the exact fonts:

1. Create a project at fonts.adobe.com with `freight-text-pro` (500, 700), `adobe-caslon-pro` (400, 700, italics) and `freight-sans-pro` (500).
2. Add your domain to the project.
3. Paste the project's `<link rel="stylesheet" href="https://use.typekit.net/xxxxxxx.css">` into the `<head>` template in `build.py`, then rebuild.

The CSS already lists these font families first, so no other changes are needed.

## Media

Images still load from the Squarespace CDN (`images.squarespace-cdn.com`), at the same sizes and with the same `srcset` widths. The videos are the same Vimeo embeds. If the Squarespace site is closed, download the images into `assets/img/` and update the paths in `build.py`.

## Forms

- **Contact form:** posts with `mailto:` to info@SantaCruzNursery.com. Swap the `action` for a form service (Formspree, Netlify Forms and so on) for real submissions.
- **Newsletter:** the live block has no storage set up, so this one doesn't submit either.

## Deploy

GitHub Pages: Settings → Pages → Deploy from branch → `main` / root.
