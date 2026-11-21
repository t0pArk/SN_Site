#!/usr/bin/env python3
"""Static site generator for the Santa Cruz Nursery & Farm rebuild.

Every section / block below mirrors the live Squarespace page:
  * grid areas ("row/col/row/col") come straight from Squarespace's fluid engine
    (mobile = 8-column grid, desktop >= 768px = 24-column grid)
  * pt/pb are section paddings in Squarespace spacing units (see --u in site.css)
  * minh is the section min-height in vh

Run:  python3 build.py   (writes the HTML files next to this script)
"""
import html
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
CDN = "https://images.squarespace-cdn.com/content/v1/634b03b7466c7152108e6885/"
SITE = "Santa Cruz Nursery & Farm"
FAVICON = CDN + "3fe95b3d-f470-48ac-84a9-4a6e059eb001/favicon.ico?format=100w"
LOGO = CDN + "03f86b4d-af8e-4996-945f-d536b7a79203/SantaCruz_nurseryLogo_Black+Transparent.png"

# Path the site is served from. "/SN_Site/" for https://<user>.github.io/SN_Site/, "/" on a custom domain.
BASE_PATH = os.environ.get("BASE_PATH", "/SN_Site/")

NAV = [("Our Story", "/"), ("Wholesale", "/wholesale"), ("Plants", "/plants"), ("FAQs", "/faqs")]


# ---------------------------------------------------------------- helpers
def img(src, alt="", sizes="100vw", cls="", eager=False):
    base = src if src.startswith("http") else CDN + src
    srcset = ", ".join(f"{base}?format={w}w {w}w" for w in (500, 750, 1000, 1500, 2500))
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{base}?format=1500w" srcset="{srcset}" sizes="{sizes}" '
            f'alt="{html.escape(alt)}" {load} decoding="async">')


def T(m, d, html_, z=0, j="flex-start/flex-start", scaled=False):
    return dict(t="text", m=m, d=d, z=z, j=j, html=html_, scaled=scaled)


def I(m, d, src, z=0, j="center/center", href=None, fit="cover", alt=""):
    return dict(t="image", m=m, d=d, z=z, j=j, src=src, href=href, fit=fit, alt=alt)


def B(m, d, text, href, style="primary", z=0, j="center/center"):
    return dict(t="button", m=m, d=d, z=z, j=j, text=text, href=href, style=style)


def E(m, d, src, z=0, j="flex-start/flex-start"):
    return dict(t="embed", m=m, d=d, z=z, j=j, src=src)


def A(m, d, items, z=0, j="flex-start/flex-start", first_open=True):
    return dict(t="accordion", m=m, d=d, z=z, j=j, items=items, first_open=first_open)


def X(kind, m, d, z=0, j="flex-start/flex-start", **kw):
    return dict(t=kind, m=m, d=d, z=z, j=j, **kw)


def S(theme, rows, blocks, minh=0, pt=0, pb=0, valign="middle", bg=None, ov=0.15, pt_gutter=False):
    return dict(kind="fe", theme=theme, rows=rows, blocks=blocks, minh=minh, pt=pt, pb=pb,
                valign=valign, bg=bg, ov=ov, pt_gutter=pt_gutter)


# ---------------------------------------------------------------- page data
VIMEO_STORY = "https://player.vimeo.com/video/760829128?h=6377d03929&autoplay=1&loop=1&title=0&byline=0&portrait=0"
VIMEO_WHOLESALE = "https://player.vimeo.com/video/760852167?h=3ed94d5978&autoplay=1&loop=1&title=0&byline=0&portrait=0"

HOME = [
    S("black-bold", (6, 10), minh=66, pt=6.6, pb=6.6,
      bg="5c71e155-a31a-4ecb-ad76-23ca7cf5af86/download-9.jpg", blocks=[
          T("1/2/5/10", "1/2/7/26",
            '<h2 style="text-align:center" class="pre"><strong>Cultivating the splendor of California’s Central Coast takes generational know-how, big vision, and a passion for growing what people love.</strong></h2>'),
          B("5/4/7/8", "7/12/9/16", "LEARN MORE", "/wholesale", style="secondary", z=1),
      ]),
    S("dark", (13, 28), minh=33, pt=3.3, pb=3.3, blocks=[
        T("1/3/4/9", "1/6/7/22", '<h3 style="text-align:center">Our Story</h3>', j="center/center", scaled=True),
        E("4/2/12/10", "5/2/25/26", VIMEO_STORY, z=1),
        T("12/2/14/10", "25/2/29/26",
          '<h2 class="pre">Located in Santa Cruz County, our farms enjoy privileged positions along the Monterey Bay coastline.</h2>', z=2),
    ]),
    S("white", (20, 21), blocks=[
        T("2/2/5/8", "6/2/8/12", '<h2 class="pre">California Central Coast</h2>', z=1),
        T("5/2/10/10", "8/2/16/10",
          '<p class="pre">Cool nights, sunny days and coastal breezes make our land ideal for growing crops that require moderate Mediterranean conditions to flourish. Redolent of wet, salty air and sun-soaked mornings, our plants are living legacies to the storied beauty of the California Central Coast and the farmers who have cultivated it for generations.</p>', z=4),
        I("11/1/21/11", "1/14/22/27", "d96119f1-0a79-4c97-81cd-00d9a4aa8e37/download-9.jpg"),
    ]),
    dict(kind="list", theme="dark", title="Fan Favorites", items=[
        ("European Cypress", "a4604ce2-b269-44b7-9c2a-266f22b80c7a/download-22.jpg", None, None),
        ("Lemon Cypress", "0b45a38c-ae5f-4412-971c-34be11e8f85d/download-21.jpg", "See More", "/new-page-1"),
        ("Lavender", "854f28b3-901b-486e-b4e4-b03d9a7662e0/download-20.jpg", None, None),
    ]),
    S("black", (4, 8), minh=33, pt=3.3, pb=3.3,
      bg="8d25c7f5-8f94-4791-91ad-e29b1b4a55aa/download-8.jpg", blocks=[
          T("1/2/3/10", "1/2/7/17",
            '<h3 class="pre"><span class="sqsrte-text-color--black">From cultivating a one-of-a-kind heather to merchandising solutions that make shoppers stop and take notice, every aspect of our operation is rooted in innovation.</span></h3>', z=1),
          B("3/2/5/10", "7/2/9/6", "Contact us", "/contact-us", z=2),
      ]),
]

LOGOS = [
    ("4/2/10/10", "10/20/17/26", "41c1912f-df11-4729-a683-a16c9046ed6a/Screen+Shot+2022-10-15+at+2.56.29+PM.png", 11),
    ("10/2/16/10", "3/8/10/14", "a76d87bf-44b8-4ce1-b126-046c39704537/Screen+Shot+2022-10-15+at+2.56.20+PM.png", 12),
    ("16/2/22/10", "3/14/10/20", "8894a1a5-4ade-4b49-9b82-ed605c6c1c8c/Screen+Shot+2022-10-15+at+2.56.24+PM.png", 12),
    ("22/2/28/10", "3/20/10/26", "ba501160-c67a-4f98-b796-ff60a4abcb18/Screen+Shot+2022-10-15+at+2.56.39+PM.png", 12),
    ("28/2/34/10", "10/8/17/14", "16680224-d0bf-44e0-ac10-ad7b2cfd38eb/Screen+Shot+2022-10-15+at+2.56.43+PM.png", 12),
    ("34/2/40/10", "10/2/17/8", "2c395e63-1ffc-4d69-aeb6-c071720e456c/Screen+Shot+2022-10-15+at+2.56.14+PM.png", 13),
    ("40/2/46/10", "10/14/17/20", "ea32f511-65d3-4b7f-96be-a8afb08ae4c1/Screen+Shot+2022-10-15+at+2.56.47+PM.png", 13),
    ("46/2/52/10", "3/2/10/8", "73d80f93-9186-40e1-8bbd-aa1eadabaca4/Screen+Shot+2022-10-15+at+2.56.08+PM.png", 14),
]

WHOLESALE = [
    S("black-bold", (9, 5), minh=66, pb=13.2, pt_gutter=True, valign="top",
      bg="e704f0fd-5796-4b67-ab1e-eee32301e590/1.png", blocks=[
          T("1/2/9/10", "1/4/6/24", '<h1 style="text-align:center" class="pre">A niche grower with formidable capabilities</h1>'),
      ]),
    S("dark", (16, 10), minh=52, pt=5.2, pb=5.2, blocks=[
        T("1/2/15/10", "1/2/8/26",
          '<h3 style="text-align:center" class="pre">Offering unique products with consistently high sell-through rates, our wholesale operation is growing with new crops and products added seasonally to meet demand. Our reputation for delivering ingenious products that consumers love is why the nation’s top distributors, grocers and home centers turn to us.</h3>'),
        B("15/2/17/10", "9/12/11/16", "View Products", "/plants", z=1),
    ]),
    S("white", (8, 5), minh=1, pt=0, pb=0.2, valign="top", blocks=[
        E("1/2/9/10", "1/1/6/27", VIMEO_WHOLESALE, z=1),
    ]),
    S("white", (51, 16), minh=30, pt=3, pb=3, blocks=[
        T("1/2/4/10", "1/2/3/26", '<h4 style="text-align:center" class="pre">Companies who trust us </h4>', z=15, j="flex-start/center"),
    ] + [I(m, d, src, z=z, fit="contain", alt="") for (m, d, src, z) in LOGOS]),
    S("white", (38, 38), minh=33, pt=3.3, pb=3.3, blocks=[
        I("1/2/9/10", "1/2/19/14", "1665900917627-IW9NHG31XZORC64LD9XD/unsplash-image-x8ZStukS2PM.jpg", z=2),
        T("9/2/15/10", "1/16/17/24",
          '<h3 class="pre">Logistics that go the extra mile</h3><p class="pre">Unique to other niche growers, we have the capabilities for direct-to-store delivery for customers who don’t want to hold product in distribution centers. Our Federal Express program allows us to harvest and deliver product within three days, guaranteed. A minimum of four or five cases per location is required. We work closely with all of our logistic companies to insure that the freshness and quality of the products you receive are to our high standards</p>',
          j="center/flex-start"),
        I("16/2/24/10", "24/13/39/25", "1665900951219-4QYLAO09UMQ7EGKI656L/unsplash-image-c23Lv2fzEyo.jpg", z=5),
        T("24/2/30/10", "24/4/34/12",
          '<h3 class="pre">Green thumbs optional</h3><p class="pre">Our specialists are available to answer plant care questions that may arise at the store level. Upon request, Santa Cruz Nursery products come with unpacking and care instructions so plants stay healthy and vibrant in store. Our informative plant care tags ensure consumer success once plants are brought home.</p>',
          z=3, j="center/flex-start"),
        B("30/2/32/10", "17/16/19/20", "Contact us", "/contact-us", z=6),
        B("32/2/34/10", "34/4/36/8", "View Products", "/plants", z=7),
    ]),
]

PLANT_TILES = [
    # (mobile img, desktop img, mobile title, desktop title, image, href, label, z_img, z_title)
    ("1/2/12/10", "1/2/12/10", "12/2/14/10", "12/2/14/10", "44cfb46f-031d-4b88-9b59-16abac7148ee/download-21.jpg", "/lemon-cypress", "Lemon Cypress", 0, 1),
    ("14/2/25/10", "1/10/12/18", "25/2/27/10", "12/10/14/18", "5a0bf751-be89-4766-a215-79d798f52779/download-20.jpg", "/lavender", "Lavender", 3, 4),
    ("27/2/38/10", "1/18/12/26", "38/2/40/10", "12/18/14/26", "f410e92a-0835-4cee-83c5-d672883a3562/download-23.jpg", "/rosemary", "Rosemary", 6, 7),
    ("40/2/51/10", "14/2/25/10", "51/2/53/10", "25/2/27/10", "f34d8ea9-f4b1-4380-9a1b-1f1a62b1f717/download-22.jpg", "/european-cypress", "European Cypress", 1, 2),
    ("53/2/64/10", "14/10/25/18", "64/2/66/10", "25/10/27/18", "7eb67dcd-1aa1-437c-a1fa-b9a11dc64ad5/091219_coastal-steel_684.jpg", "/angel-vine", "Angel Vine", 4, 5),
    ("66/2/77/10", "14/18/25/26", "77/2/79/10", "25/18/27/26", "64f31f33-2227-40f9-938d-08623a450a77/download-2.jpg", "/edibles", "Edibles", 7, 8),
    ("79/2/90/10", "27/2/38/10", "90/2/92/10", "38/2/40/10", "43b84082-dd58-4755-a73d-a8c46b766967/download-6.jpg", "/hellebores", "Hellebores", 2, 3),
    ("92/2/103/10", "27/10/38/18", "103/2/105/10", "38/10/40/18", "43b84082-dd58-4755-a73d-a8c46b766967/download-6.jpg", "/italian-ventricosa", "Italian Ventricosa", 5, 6),
]
plant_blocks = []
for (mi, di, mt, dt, src, href, label, zi, zt) in PLANT_TILES:
    plant_blocks.append(I(mi, di, src, z=zi, href=href, alt=label))
    plant_blocks.append(T(mt, dt, f'<h4 class="pre"><a href="{href}">{label}</a></h4>', z=zt, j="center/center"))

PLANTS = [
    S("black-bold", (11, 10), minh=10, pt_gutter=True, pb=0, valign="top",
      bg="919585d9-536a-4615-a53b-549d3bae5e62/Screen+Shot+2022-10-16+at+1.26.15+PM.png", blocks=[
          T("2/2/11/10", "4/2/10/20",
            '<h2 class="pre">Grown in the diverse microclimates of the Monterey Bay, our plants form the basis of 100+ signature and seasonal products.</h2>',
            j="center/center"),
      ]),
    S("dark", (104, 40), minh=33, pt=3.3, pb=3.3, blocks=plant_blocks),
]

FAQ_ITEMS = [
    ("Do you provide any in-store merchandising?", "We offer an array of merchandising solutions, including displays and specialty packaging, upon request. Contact our sales team for more information."),
    ("Do your products come with consumer care instructions?", "Yes, all of our products include care tags to ensure customer success with our plants at home."),
    ("Do your products come with store unpacking and care instructions?", "We are happy to provide in-store care resources, including unpacking instructions, upon request."),
    ("How long will it take for my order to arrive?", "We ship on Monday and Tuesday to ensure Thursday and Friday delivery. Please note that orders must be placed in advance in order to ensure availability."),
    ("Do you offer direct-to-store delivery?", '<a href="/contact-us">Contact </a>our sales team for more information.'),
    ("When is the Ventricosa Heather available?", "Our famed heather blooms from late April through May. Its rare, fleeting beauty, is part of its unmistakable appeal."),
]

FAQS = [
    S("white", (11, 14), blocks=[
        I("1/1/10/11", "1/1/15/27", "ae4829d7-fb65-4bec-af15-6ddd649739d6/download-10.jpg"),
        T("4/2/8/10", "7/8/10/20", '<h1 style="text-align:center" class="pre"><span class="sqsrte-text-color--white">FAQ</span></h1>', z=1),
        T("10/2/12/10", "9/11/11/17", '<p style="text-align:center" class="pre"><span class="sqsrte-text-color--white">Frequently Asked Questions</span></p>', z=2),
    ]),
    S("white", (12, 22), minh=66, pt=6.6, pb=6.6, blocks=[
        A("2/2/7/10", "1/13/23/26", FAQ_ITEMS, z=1, first_open=False),
        I("7/2/13/10", "1/2/19/12", "1665901035406-R4JDXRNKZ23E68A3T2HK/unsplash-image-BduDcrySLKM.jpg", z=2),
    ]),
]

CONTACT = [
    S("white", (2, 3), bg="0915f09e-10cb-42bc-9d8f-c30d2c4f28e2/download-53.jpg", blocks=[]),
    S("dark", (32, 22), minh=33, pt=3.3, pb=3.3, blocks=[
        T("1/2/7/10", "1/2/8/12",
          '<h2 class="pre">Contact us.</h2><p class="pre"><strong>Email: </strong>info@SantaCruzNursery.com</p><p class="pre"><strong>Phone:</strong> (831) 722-6680</p><p class="pre"><strong>Address:</strong> 117 Rancho road Watsonville, CA 95076</p>'),
        X("form", "7/2/21/10", "9/2/23/14", z=2),
        X("map", "21/2/33/10", "1/15/23/26", z=3, q="117 Rancho Rd, Watsonville, CA 95076"),
    ]),
]


def plant_page(name, rows, grid, image, text, items, carousel):
    """grid = (h1_m, h1_d, img_m, img_d, p_m, p_d, acc_m, acc_d, btn_m, btn_d)"""
    g = grid
    secs = [S("white", rows, blocks=[
        T(g[0], g[1], f'<h1 class="pre">{name}</h1>', z=1),
        I(g[2], g[3], image, z=4, alt=name),
        T(g[4], g[5], f'<p class="pre">{text}</p>', z=3),
        A(g[6], g[7], items, z=2),
        B(g[8], g[9], "Back to products", "/plants", z=6),
    ])]
    if carousel:
        secs.append(dict(kind="carousel", theme="white", images=carousel))
    return secs


P = "/"  # helper for readability
PLANT_PAGES = {
    "european-cypress": ("European Cypress", (33, 26),
        ("2/2/6/10", "3/2/6/13", "6/2/12/10", "1/17/27/27", "12/2/17/10", "6/2/9/16", "17/2/32/10", "9/2/24/16", "32/2/34/10", "25/2/27/7"),
        "c07f543e-6dd2-43e4-915a-63997c93e15c/download-33.jpg",
        "Native to the western United States and useful as a single tree, hedge or patio container plant. Decorate it year after year as a living Christmas tree.",
        [("Size", "Up to 15 feet tall and 5 feet wide."),
         ("Planting Guide", "Enjoy indoors during the holidays then plant outside in the garden or leave in the pot. Well drained soil. Can be transplanted to larger containers for the patio."),
         ("Light", "Partial shade to full sun."),
         ("Temperature", "USDA Zones 6–9. Hardy down to -5℉ for established plants in the ground. Tolerant to 115℉."),
         ("Water", "Keep moist to establish. Light watering to maintain. Plant where soil stays dry to moist, but not soggy."),
         ("Feeding", "Fertilize in the spring and fall during growth. Prefers acid soils."),
         ("Product", "Available October–December, our potted European Cypress comes in a variety of sizes and presentations, including seasonal decor. See catalogue for complete product listing including size, quantities, availability and UPCs.")],
        ["2193f2fc-43ba-49e9-94c2-e36ef15a10de/download-34.jpg", "9313c86a-708e-440c-aa4e-0b0d67473291/download-35.jpg",
         "0f86abd9-26c0-4f4f-b7bc-84d341ed7e6a/download-4.jpg", "abe98176-dfdf-480f-a240-68c5f961d8c3/download-36.jpg"]),
    "lemon-cypress": ("Lemon Cypress", (31, 27),
        ("2/2/4/10", "3/2/6/13", "4/2/10/10", "1/17/27/27", "10/2/15/10", "6/2/10/16", "15/2/30/10", "10/2/25/16", "30/2/32/10", "26/2/28/7"),
        "2abe392f-a1dc-4c24-a52b-fb8ecf68eab8/download-41.jpg",
        "Native to California’s Monterey Peninsula, this fast-growing, lemon-scented plant has multiple uses in the home, patio and landscape. It will keep its conical shape until 30 feet tall.",
        [("Size", "Up to 30 feet tall and 20 feet wide."),
         ("Planting Guide", "In the garden, plant in well-drained soil in early spring before the heat of summer, or plant in early fall. Prune if needed for hedges or to keep smaller. For container growing, transplant to a larger pot to allow for growth and easier water management."),
         ("Light", "Partial shade in hot areas. Full sun in moderate coastal zones."),
         ("Temperature", "0℉ to 105℉. USDA Zones 7–10."),
         ("Water", "Keep well watered but not soggy. Can dry quickly in the pot. Be careful to avoid excessive drying or plant may not recover."),
         ("Feeding", "During spring and summer growth, feed with a balanced fertilizer."),
         ("Product", "Available October–December, our potted Lemon Cypress comes in a variety of sizes and presentations, including seasonal decor. See catalogue for complete product listing including size, quantities, availability and UPCs.")],
        ["1665881566593-GTTHOM3B9WTV7QS9K98Y/download-43.jpg", "1665881583990-7TARSCDKMMFNK2ICOELV/download-44.jpg",
         "1665881432800-7RNC0UY0CW9D2XQVCXQY/download-21.jpg", "1665881515457-IS70LEE4YQX508DUBUKZ/download-42.jpg"]),
    "lavender": ("Lavender", (31, 26),
        ("2/2/4/10", "3/2/6/13", "4/2/10/10", "1/17/27/27", "10/2/15/10", "6/2/9/16", "15/2/30/10", "9/2/24/16", "30/2/32/10", "25/2/27/7"),
        "66247487-0977-4d98-9337-49748045764c/download-37.jpg",
        "Mediterranean native with aromatic foliage. Flowers can be purple, pink or white depending on variety. Flowers in the spring and summer, attracting bees.",
        [("Size", "1 to 3 feet tall with a similar width."),
         ("Planting Guide", "Enjoy indoors for a few weeks but eventually should be planted outdoors in containers or the garden. Well-drained soil. Can be sheared back no more than half."),
         ("Light", "Full sun. Provide some protection from the afternoon sun in very hot climates."),
         ("Temperature", "Cool nights, warm days. Most varieties established in the ground can tolerate down to 15℉. Plants in containers will be more sensitive to cold."),
         ("Water", "Drought tolerant. Water thoroughly but allow to dry between watering."),
         ("Feeding", "Very little fertilizer is required, if any."),
         ("Product", "Our potted Lavender come in a variety of sizes and presentations, including decorative wraps and containers. See catalogue for complete product listing including size, quantities, availability and UPCs.")],
        ["14673b25-d67c-499a-8b0c-ff2274eeb3d3/download-37.jpg", "9d53e81c-1d27-4aa5-8a62-0193984c3c35/download-39.jpg",
         "d2b9cf89-af85-488b-9006-326e436a5e2a/download-6.jpg", "a8f2e1c1-c811-4923-8980-2f934d0b7c52/download-40.jpg"]),
    "rosemary": ("Rosemary", (31, 26),
        ("2/2/4/10", "3/2/6/13", "4/2/10/10", "1/17/27/27", "10/2/15/10", "6/2/9/16", "15/2/30/10", "9/2/24/16", "30/2/32/10", "25/2/27/7"),
        "298cb3af-82d8-4498-b590-4f7b3a839906/download-45.jpg",
        "A Mediterranean native, the aromatic leaves of this plant are often used in cooking. Small clusters of blue flowers in winter and spring attract birds and bees.",
        [("Size", "2 to 6 feet"),
         ("Planting Guide", "Enjoy indoors for a month or two but eventually should be outdoors in containers or the garden. Well drained soil. Prune to shape as desired."),
         ("Light", "Bright sun for 6 to 8 hours."),
         ("Temperature", "Established plants in the ground can tolerate 20℉ but protect or bring in smaller containers when below 30℉ as roots are more sensitive to cold."),
         ("Water", "In pot, water thoroughly but allow soil to dry slightly between watering. In the garden, keep on the dry side."),
         ("Feeding", "Feed lightly during periods of growth."),
         ("Product", "Our potted Rosemary comes in a variety of sizes and presentations, including seasonal decor. See catalogue for complete product listing including size, quantities, availability and UPCs.")],
        ["4dd8bb2d-fbb5-4534-af48-72607348e83b/download-46.jpg", "d7db687d-6c0c-40c7-a8cf-1098af1d05b9/download-47.jpg",
         "f9554d5f-3884-433e-955f-ce6820614b91/download-5.jpg", "7b59c958-4f83-4411-8a23-5c8f4d7d4d02/download-48.jpg"]),
    "angel-vine": ("Angel Vine", (31, 27),
        ("2/2/4/10", "3/2/6/13", "4/2/10/10", "1/17/27/27", "10/2/15/10", "6/2/10/16", "15/2/30/10", "10/2/25/16", "30/2/32/10", "26/2/28/7"),
        "44f11735-3a00-43c8-b046-eb33db69a53d/download-26.jpg",
        "Native to New Zealand, Angel Vine is a long vining plant with small round leaves. It thrives in average household conditions and lends itself to metal frames and topiary designs.",
        [("Size", "8″H, 6″ diameter"),
         ("Planting Guide", "Angel vine, soil, preserved sheet moss, metal pot, plastic liner"),
         ("Light", "Keep indoors with bright or direct sunlight"),
         ("Temperature", "Prefers indoor or sheltered outdoor setting at room temperature (65-80 degrees F). Avoid drafts, vents, and temperature extremes."),
         ("Water", "Water thoroughly to keep soil evenly moist. Outer pot does not drain. Remove grower’s pot when watering and allow excess water to drain before replacing."),
         ("Feeding", "Add plant fertilizer every 6 months."),
         ("Product", "We offer several Angel Vine products including topiary, trees, hearts and rings in various sizes and presentations. See our catalog for complete product listing including size, quantities, availability and UPCs.")],
        ["fb0b50e1-ed61-4aca-b4de-6c8e74500fc7/download-24.jpg", "b36b0f59-fffd-4524-9f6f-86b010a51dc5/download-27.jpg",
         "12120ff3-44af-4d0c-8c4e-9e4b9186bc53/download-28.jpg"]),
    "edibles": ("Edibles", (30, 27),
        ("1/2/3/10", "3/2/6/13", "3/2/9/10", "1/17/27/27", "9/2/14/10", "6/2/9/16", "14/2/29/10", "9/2/24/16", "29/2/31/10", "25/2/27/7"),
        "e3a7ddb4-d65e-4070-9805-6ce1c939e1a0/download-32.jpg",
        "Available March–May, our high-antioxidant Heart Healthy Plants include blueberries, blackberries, raspberries, grapes, and pomegranates.",
        [("Size", "4 inches tall in pot."),
         ("Planting Guide", "Plant in a sunny area with good air circulation and well-drained soil. See individual plant care tags for further instructions."),
         ("Light", "Full sun"),
         ("Temperature", "See individual plant care tags for details."),
         ("Water", "Minimal to above average. See individual plant care tags for details."),
         ("Feeding", "See plant care tag"),
         ("Product", "These popular small format edibles come in a three-level retail-ready display containing 180 plants. See catalogue for complete product listing including size, quantities, availability and UPCs.")],
        ["691c2e2e-b020-447f-a53b-8a93353025c7/download-3.jpg", "6b384640-78f4-4858-a496-015487bc77bc/download-30.jpg",
         "6b73d889-0bbd-4216-aa84-1c1335b3d569/download-31.jpg", "5902ccde-34bc-4581-9f98-27d05e4803d6/download-29.jpg"]),
    "hellebores": ("Hellebores", (31, 29),
        ("1/2/3/10", "3/2/6/13", "3/2/9/10", "1/17/27/27", "9/2/14/10", "6/2/10/16", "14/2/29/10", "10/2/25/16", "29/2/31/10", "27/2/29/7"),
        "79c9dc7d-4ae4-43fc-a40e-3c77b361061e/download-7.jpg",
        "Primarily native to the Balkan Peninsula, these winter-hardy shade perennials produce beautiful long-lasting winter and spring flowers in colors of pink, green, white and purple, depending on variety.",
        [("Size", "18 inches tall and 2 feet wide"),
         ("Planting Guide", "Enjoy in containers on the deck or balcony. Pots will eventually become root-bound so plant into the garden under larger trees or house eaves in filtered light or shade. Soil should have plenty of organic matter and drain well. Prefer neutral to alkaline soil. Will develop seeds and self-sow. Seedlings flower in 2–3 years."),
         ("Light", "Partial or full shade"),
         ("Temperature", "-15℉ to 90℉. Hellebores can survive warm weather but will tend to go dormant. Not for desert climates."),
         ("Water", "Evenly moist soil. Well-established plants in the ground can tolerate some drought"),
         ("Feeding", "Use a balanced fertilizer during early spring at half of label rates."),
         ("Product", "See catalogue for complete product listing including size, quantities, availability and UPCs.")],
        []),
    "italian-ventricosa": ("Italian Ventricosa", (34, 29),
        ("2/2/4/10", "3/2/6/13", "4/2/10/10", "1/17/27/27", "10/2/16/10", "6/2/11/16", "16/2/32/10", "11/2/26/16", "32/2/34/10", "27/2/29/7"),
        "e9e13454-3857-4198-8ac7-1732820882fa/download-7.jpg",
        "The plant that first put us on the map, the Italian Ventricosa is a Santa Cruz Nursery exclusive. Native to South Africa, this showy plant with bonsai-like green foliage prefers everything in moderation. Fills with a bounty of bright pink blooms just in time for Mothers Day.",
        [("Size", "1 ½ feet to 3 ½ feet. Spreads 20 to 30 inches."),
         ("Planting Guide", "Plant outdoors in the garden in USDA Zones 10–11 or display indoors. In climates suitable for planting outdoors, it can be grown in a container and moved to avoid extreme hot or cold conditions."),
         ("Light", "Full sun in moderate coastal climates. Partial sun in warmer climates."),
         ("Temperature", "55℉ to 80℉ but will tolerate down to 30℉. This plant is considered a perennial in moderate climates only."),
         ("Water", "Excellent drainage and acid soil. Heavy clay soil is usually fatal. No standing water on roots. Avoid drying in pots."),
         ("Feeding", "Give light feeding of acid plant food in early spring."),
         ("Product", "Available late April through May, our Italian Ventricosa comes potted and wrapped in decorative paper. See catalogue for complete product listing including size, quantities, availability and UPCs.")],
        []),
}

FOOTER = S("black", (28, 13), minh=5, pt=0, pb=1, valign="top", blocks=[
    T("2/2/5/10", "2/2/4/14",
      '<p class="pre footer-links"><a href="/our-story">Our Story</a>     <a href="/wholesale">Wholesale</a>      <a href="/plants">Plants</a>      <a href="/faqs">FAQ</a>      <a href="/contact-us">Contact us</a></p>'),
    T("5/2/17/10", "4/2/12/14",
      '<h3 class="pre">Santa Cruz Nursery &amp; Farm</h3><p class="sqsrte-small pre">We are a wholesale grower of select crops suited to the microclimates of California’s Monterey Bay. With operations across seven farms and more than 140 acres, our specialties include several varieties of cypress and the rare ventricosa heather. Many of the nation’s top grocers and home centers have trusted us for highly differentiated products, innovative merchandising solutions and superior logistics that result in exceptional sell-through rates.</p>'),
    X("newsletter", "17/2/28/10", "3/15/11/26"),
    T("27/2/29/10", "12/17/14/26", '<p style="text-align:right" class="sqsrte-small pre">Copyright © 2022 Santa Cruz Nursery &amp; Farm</p>'),
])

PAGES = [
    # (output path, title, active nav href, sections)
    ("index.html", SITE, "/", HOME),
    ("our-story/index.html", SITE, "/", HOME),
    ("wholesale/index.html", f"General 1 — {SITE}", "/wholesale", WHOLESALE),
    ("plants/index.html", f"Plants — {SITE}", "/plants", PLANTS),
    ("faqs/index.html", f"FAQs 2 — {SITE}", "/faqs", FAQS),
    ("contact-us/index.html", f"Contact 1 — {SITE}", "/contact-us", CONTACT),
] + [
    (f"{slug}/index.html", f"{d[0]} — {SITE}", "/plants", plant_page(*d)) for slug, d in PLANT_PAGES.items()
]


# ---------------------------------------------------------------- rendering
class R:
    def __init__(self, depth):
        self.pre = "../" * depth

    def url(self, href):
        if not href or href.startswith(("http", "mailto:", "tel:", "#")):
            return href
        path = href.strip("/")
        return (self.pre or "./") + (path + "/" if path else "")

    def links(self, s):
        # rewrite root-relative hrefs inside an HTML fragment
        import re
        return re.sub(r'href="(/[^"]*)"', lambda m: f'href="{self.url(m.group(1))}"', s)


def area(m, d, z):
    return f"--m:{m};--d:{d};--z:{z}"


def jvars(j):
    jm, _, jd = j.partition("/")
    return f";--jm:{jm};--jd:{jd or jm}"


def render_block(b, r):
    style = area(b["m"], b["d"], b["z"]) + jvars(b["j"])
    t = b["t"]
    if t == "text":
        inner = r.links(b["html"])
        if b.get("scaled"):
            inner = f'<span class="scaled-text">{inner}</span>'
        body = f'<div class="html-content">{inner}</div>'
    elif t == "image":
        pic = img(b["src"], b["alt"], sizes="(min-width: 768px) 50vw, 100vw")
        if b["href"]:
            pic = f'<a href="{r.url(b["href"])}">{pic}</a>'
        body = f'<div class="img-wrap" style="--fit:{b["fit"]}">{pic}</div>'
    elif t == "button":
        body = (f'<div class="btn-wrap"><a class="btn btn--{b["style"]}" href="{r.url(b["href"])}">'
                f'{html.escape(b["text"])}</a></div>')
    elif t == "embed":
        body = (f'<div class="ratio"><iframe src="{html.escape(b["src"])}" title="Video" '
                f'allow="autoplay; fullscreen; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>')
    elif t == "accordion":
        lis = []
        for i, (q, a) in enumerate(b["items"]):
            open_ = b["first_open"] and i == 0
            lis.append(
                f'<li class="{"open" if open_ else ""}"><h4><button class="accordion-btn" aria-expanded="{"true" if open_ else "false"}">'
                f'<span>{q}</span><i class="accordion-icon" aria-hidden="true"></i></button></h4>'
                f'<div class="accordion-panel"><div><div class="accordion-desc"><p class="pre">{r.links(a)}</p></div></div></div></li>')
        body = f'<ul class="accordion">{"".join(lis)}</ul>'
    elif t == "form":
        req = '<span class="req">(required)</span>'
        body = f'''<form action="mailto:info@SantaCruzNursery.com" method="post" enctype="text/plain">
  <fieldset class="form-item"><legend>Name</legend>
    <div class="form-row">
      <div><label><span class="sub">First Name</span>{req}<input class="field" type="text" name="fname" autocomplete="given-name" required></label></div>
      <div><label><span class="sub">Last Name</span>{req}<input class="field" type="text" name="lname" autocomplete="family-name" required></label></div>
    </div>
  </fieldset>
  <div class="form-item"><label><span class="title">Email</span>{req}<input class="field" type="email" name="email" autocomplete="email" required></label></div>
  <fieldset class="form-item"><legend>Phone (optional)</legend><input class="field" type="tel" name="phone" autocomplete="tel" aria-label="Phone"></fieldset>
  <div class="form-item"><label><span class="title">Message</span>{req}<textarea class="field" name="message" required></textarea></label></div>
  <button class="btn btn--primary" type="submit">Send</button>
</form>'''
    elif t == "map":
        q = html.escape(b["q"]).replace(" ", "+")
        body = (f'<iframe src="https://maps.google.com/maps?q={q}&amp;z=13&amp;output=embed" '
                f'title="Map" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>')
    elif t == "newsletter":
        body = '''<form class="newsletter" onsubmit="return false">
  <p>Sign up with your email address to receive news and updates.</p>
  <div class="newsletter-row">
    <label class="sr-only" for="nl-email">Email Address</label>
    <input id="nl-email" type="email" name="email" placeholder="Email Address" autocomplete="email">
    <button class="btn btn--primary" type="submit">Sign Up</button>
  </div>
</form>'''
    else:
        raise ValueError(t)
    return (f'<div class="fe-block" style="{style}"><div class="sqs-block {t}-block">{body}</div></div>')


ARROW = ('<svg viewBox="0 0 44 18" aria-hidden="true"><path d="M9.90649 16.96L2.1221 9.17556L9.9065 1.39116"/>'
         '<path d="M42.8633 9.18125L3.37868 9.18125"/></svg>')


def render_section(s, r):
    theme = f'theme-{s["theme"]}'
    if s["kind"] == "list":
        items = []
        for (title, src, btn, href) in s["items"]:
            b = (f'<div class="btn-wrap"><a class="btn btn--primary" href="{r.url(href)}">{btn}</a></div>' if btn else "")
            items.append(f'<li class="list-item"><div class="media">{img(src, title, sizes="(min-width: 768px) 33vw, 100vw")}</div>'
                         f'<h2>{title}</h2>{b}</li>')
        return (f'<section class="page-section list-section {theme}"><div class="list-inner">'
                f'<div class="list-title"><p class="pre">{s["title"]}</p></div>'
                f'<ul class="list-grid">{"".join(items)}</ul></div></section>')
    if s["kind"] == "carousel":
        items = "".join(f'<li class="carousel-item"><div class="media">{img(src, "", sizes="(min-width: 768px) 25vw, 100vw")}</div></li>'
                        for src in s["images"])
        return (f'<section class="page-section carousel-section {theme}"><div class="carousel-inner"><div class="carousel">'
                f'<button class="carousel-arrow prev" aria-label="Previous">{ARROW}</button>'
                f'<div class="carousel-viewport"><ul class="carousel-track">{items}</ul></div>'
                f'<button class="carousel-arrow next" aria-label="Next">{ARROW}</button>'
                f'<div class="carousel-mobile-arrows"><button class="carousel-arrow prev" aria-label="Previous">{ARROW}</button>'
                f'<button class="carousel-arrow next" aria-label="Next">{ARROW}</button></div>'
                f'</div></div></section>')

    bg = ""
    if s["bg"]:
        bg = (f'<div class="section-background">{img(s["bg"], "", eager=True)}'
              f'<div class="section-background-overlay" style="--ov:{s["ov"]}"></div></div>')
    else:
        bg = '<div class="section-background"></div>'
    cls = f'page-section {theme}' + (" valign-top" if s["valign"] == "top" else "")
    style = f'--minh:{s["minh"]}vh'
    wrap_cls = "content-wrapper" + (" pt-gutter" if s["pt_gutter"] else "")
    wrap_style = f'--pt:{s["pt"]};--pb:{s["pb"]}'
    blocks = "".join(render_block(b, r) for b in s["blocks"])
    rm, rd = s["rows"]
    return (f'<section class="{cls}" style="{style}">{bg}'
            f'<div class="{wrap_cls}" style="{wrap_style}">'
            f'<div class="fluid-engine" style="--rm:{rm};--rd:{rd}">{blocks}</div></div></section>')


def render_page(path, title, active, sections):
    depth = path.count("/")
    r = R(depth)
    cur = ' aria-current="page"'
    nav = "".join(
        f'<li><a href="{r.url(h)}"{cur if h == active else ""}>{n}</a></li>' for n, h in NAV)
    mnav = "".join(f'<a href="{r.url(h)}">{n}</a>' for n, h in NAV)
    main = "\n".join(render_section(s, r) for s in sections)
    footer = render_section(FOOTER, r)
    return f'''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="icon" href="{FAVICON}">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{html.escape(title)}">
<link rel="preconnect" href="https://images.squarespace-cdn.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<!-- Fallback web fonts. For the exact fonts (Freight Text Pro, Adobe Caslon Pro, Freight Sans Pro)
     add your Adobe Fonts project <link> here; see README. -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@500;700&family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:wght@500&display=swap">
<link rel="stylesheet" href="{r.pre}assets/css/site.css">
</head>
<body>
<a class="skip-link" href="#page">Skip to Content</a>
<header class="header">
  <div class="header-inner">
    <button class="header-burger" aria-label="Open Menu" aria-expanded="false" aria-controls="mobile-menu">
      <span class="burger-box"><span></span><span></span><span></span></span>
    </button>
    <a class="header-logo" href="{r.url('/')}"><img src="{LOGO}?format=1500w" alt="{SITE}" width="154" height="70"></a>
    <nav class="header-nav" aria-label="Main"><ul>{nav}</ul></nav>
    <div class="header-cta"><a class="btn" href="{r.url('/contact-us')}">Contact us</a></div>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu">
  <nav aria-label="Mobile">{mnav}</nav>
  <a class="btn" href="{r.url('/contact-us')}">Contact us</a>
</div>
<main id="page">
{main}
</main>
<footer class="site-footer">
{footer}
</footer>
<script src="{r.pre}assets/js/site.js"></script>
</body>
</html>
'''


def render_404():
    page = render_page("404.html", SITE, None, [])
    body = ('<section class="page-section theme-dark"><div class="notfound">'
            '<p class="pre">We couldn\'t find the page you were looking for. This is either because:</p>'
            '<ul style="list-style:disc;padding-left:1.5em" class="p"><li>There is an error in the URL entered into your web browser. Please check the URL and try again.</li>'
            '<li>The page you are looking for has been moved or deleted.</li></ul>'
            f'<p>You can return to our homepage by <a href="./">clicking here</a>.</p></div></section>')
    # 404.html is served for any missing URL, so pin relative links to the site root
    page = page.replace("<head>", f'<head>\n<base href="{BASE_PATH}">', 1)
    return page.replace('<main id="page">\n\n</main>', f'<main id="page">\n{body}\n</main>')


def main():
    for path, title, active, sections in PAGES:
        out = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(out) or ROOT, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(render_page(path, title, active, sections))
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(render_404())
    print(f"Wrote {len(PAGES) + 1} pages")


if __name__ == "__main__":
    main()
