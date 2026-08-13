# Component library

Copy-paste building blocks. All classes are defined in `assets/engine/styles.css`
(the design system). Re-theme by editing the `:root` tokens there — the markup
below stays the same across brands. `{{...}}` marks per-site values.

## Table of contents
1. The `<head>` block (SEO + favicons + fonts)
2. Design tokens (`:root`)
3. Header + navigation
4. Hero (homepage)
5. 3-step inquiry wizard
6. Benefit / guarantee cards
7. Comparison table
8. Colour / material swatch grid
9. Price table
10. Gallery with filters
11. Contact form
12. Real photos with fallback
13. Footer + cookie bar + mobile CTA
14. Rating / social-proof panel (honest)

---

## 1. The `<head>` block
Set per page: title, description, canonical, og:title/description/url. Everything
else is identical across pages. The inline `js` script prevents a flash of
hidden reveal-elements and keeps content visible if JS is off (see pitfalls).

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script>document.documentElement.className+=" js";</script>
  <title>{{Localised page title | Brand}}</title>
  <meta name="description" content="{{Localised 150–160 char description}}">
  <link rel="canonical" href="https://{{domain}}/{{page}}.html">
  <meta name="theme-color" content="{{--c-dark}}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{{sk_SK}}">
  <meta property="og:title" content="{{...}}">
  <meta property="og:description" content="{{...}}">
  <meta property="og:url" content="https://{{domain}}/{{page}}.html">
  <meta property="og:image" content="https://{{domain}}/assets/img/og-image.png">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:image" content="https://{{domain}}/assets/img/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <link rel="manifest" href="site.webmanifest">
  <link rel="preload" href="css/styles.css?v={{YYYYMMDD}}" as="style">
  <link rel="stylesheet" href="css/styles.css?v={{YYYYMMDD}}">
  <!-- homepage only: <link rel="preload" href="assets/img/hero.svg" as="image"> -->
</head>
<!-- before </body> -->
<script src="js/config.js?v={{YYYYMMDD}}"></script>
<script src="js/main.js?v={{YYYYMMDD}}"></script>
```

The `?v=` on every local CSS/JS reference is **not optional**. Hosts cache JS for
days, so without it the owner edits `config.js`, keeps seeing the old phone
number, and reports the site as broken. Bump the date whenever you touch those
files, and say so in the README.

Use a **system font stack** (in the tokens) — no Google Fonts. It avoids an
external request, helps PageSpeed, and works offline. Only add a web font if the
brand truly demands it, and then self-host + `preload` it.

## 2. Design tokens (edit these to re-theme)
Top of `styles.css`. This is the single most important lever for "different
designs".

**The accent needs two shades, and mixing them up is the #1 accessibility bug.**
A brand's vivid accent is usually fine as a decorative fill but fails as a text
colour: white on `#E67E22` is only 2.85:1 where AA wants 4.5:1. So:

| token | use for | must satisfy |
|---|---|---|
| `--c-accent` | decorative fills — eyebrow bar, focus ring, swatches, icons | no text on it |
| `--c-accent-600` | accent **text** on white **and** button backgrounds with white labels | ≥ 4.5:1 vs white |
| `--c-accent-700` | hover state of those buttons | darker still |
| `--c-accent-300` | accent text **on dark** backgrounds (hero, dark sections) | ≥ 4.5:1 vs `--c-dark` |

Mid-tone greens/ambers (`--c-success`, star gold) have the same problem: keep a
darker `-700` variant for anything that is text. After re-theming, don't eyeball
it — run `node scripts/audit_browser.js --root .`, which measures every text
element at mobile and desktop widths.

Example (adjust per brand):
```css
:root{
  --c-dark:#2C3E50; --c-accent:#E67E22; --c-white:#fff;
  --c-bg:#fff; --c-bg-alt:#f5f7f9; --c-text:#2b3644; --c-muted:#64748b;
  --c-border:#e5e9ef; --c-star:#f5b301;
  --font-base:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
  --radius:14px; --container:1180px; --header-h:72px;
}
```
Derive tints/shades from the two brand colours; keep contrast AA. A bold hero,
different radius, or a serif display font instantly changes the personality
without touching component markup.

## 3. Header + navigation
Logo (also the "home" link — no separate "Home" nav item), links, phone, CTA,
hamburger. Mark the current page with `aria-current="page"`. Keep `.main-nav a`
`white-space:nowrap` so items never wrap.

Two things to get right: the header logo needs a **dark** wordmark and the
footer a **light** one (same file name, `-dark` / `-light`); and the in-nav CTA
must re-assert its own colours (`.main-nav a.btn--primary { color:#fff }`)
because `.main-nav a` is the more specific selector and otherwise paints the
button's label dark — invisible on the accent background, and only in the
*opened* mobile menu, so screenshots miss it.

The full working header is in the built site; key structure:
```html
<body>
  <a class="skip-link" href="#obsah">{{Preskočiť na obsah}}</a>
  <header class="site-header"><div class="container header-inner">
    <a class="brand" href="index.html" aria-label="{{Brand}} – {{domov}}">…logo…</a>
    <!-- logo: icon + wordmark image; footer uses logo-word-LIGHT.svg instead -->
    <!-- <img class="brand__mark" src="assets/logo-mark.svg" alt="" width="53" height="42">
         <span class="brand__text">
           <img class="brand__word" src="assets/logo-word-dark.svg" alt="{{Brand}}" width="135" height="20">
           <span class="brand__tag">{{Tagline}}</span>
         </span> -->
    <nav class="main-nav" id="main-nav" aria-label="{{Hlavná navigácia}}">
      <a href="produkty.html">{{Produkty}}</a> … 
      <a class="btn btn--primary btn--sm header-mobile-cta" href="kontakt.html">{{CTA}}</a>
    </nav>
    <div class="header-actions">
      <a class="header-phone" data-mh-tel href="tel:+000">…<span data-mh="business.phone"></span></a>
      <a class="btn btn--primary btn--sm header-desktop-cta" href="kontakt.html">{{CTA}}</a>
      <button class="nav-toggle" aria-label="{{Menu}}" aria-controls="main-nav" aria-expanded="false">…</button>
    </div>
  </div></header>
  <main id="obsah" tabindex="-1"> … </main>
```

## 4. Hero — two treatments, pick one
`.hero` (dark, gradient + accent glow) with `.hero-grid`, `<h1>`, subhead, two
CTAs (primary + ghost), a trust row and an optional rating badge (§14).

**A — image in a frame** (`.hero__media`): the photo sits beside the text in a
rounded card. Use when the photo is genuinely good and deserves to be seen whole.

**B — full-bleed photo** (`.hero__bg`): the photo fills the section, a diagonal
gradient over it carries the text. Use this for **ordinary client phone photos** —
which is most projects. The overlay hides their weaknesses and the result looks
considerably more expensive:

```html
<section class="hero">
  <div class="hero__bg" aria-hidden="true">
    <picture><source srcset="assets/img/hero-foto.webp" type="image/webp">
      <img decoding="async" fetchpriority="high" src="assets/img/hero-foto.jpg"
           onerror="this.onerror=null;this.src='assets/img/hero.svg'"
           width="1920" height="1267" alt=""></picture>
  </div>
  <div class="container"><div class="hero-grid">
    <div class="hero__content" data-reveal> …h1, subhead, CTAs, trust row… </div>
    <div class="hero__aside" data-reveal data-reveal-delay="1"> …rating badge… </div>
  </div></div>
</section>
```

Three things B gets wrong if you're careless: the photo is decorative, so it takes
`aria-hidden` on the wrapper and an empty `alt`; on mobile the text sits *on* the
photo rather than beside it, so the gradient must be far stronger (handled in the
bundled media query); and `preload` must point at the photo, not at the old hero
SVG. Crop the source from the **original** the client sent, not from the
gallery-sized copy — a 1200 px file looks soft stretched across a desktop hero.

## 5. 3-step inquiry wizard
The conversion centrepiece. Powered by `wizard.js` (reused as-is). Structure:
`#wizard` → `.wizard__steps` (stepper) → three `.wizard__panel` (step 1 & 2 are
`.opt` option cards with `data-group`/`data-value`; step 3 is a `<form>` with
city + phone) → a `.wizard__success` panel. On submit it calls the shared
`window.MH.sendLead(...)`. Copy the block from a built site verbatim and only
change the option labels/questions.

## 6. Benefit / guarantee cards
`.card` with `.card__icon` (inline SVG) + `<h3>` + `<p>`, in a `.grid.grid-3`
or `.guarantee`/`.guarantee-list` for the "what's included" block. Use inline
stroke SVG icons (no icon font) so they inherit `currentColor`.

## 7. Comparison table
`.compare > table`. Highlight the recommended column with `class="col-featured"`
on its `<th>`/`<td>` and a `.badge-top` pill. Wrap in `.compare` which scrolls
horizontally on mobile (`overflow-x:auto`). Use `<th scope="row">` on the left
column for accessibility.

## 8. Colour / material swatch grid
`.ral-grid` of `.ral` cards, each `.ral__swatch` (a coloured `div`, e.g.
`style="background:#293133"`) + `.ral__meta` (name + code). For a "custom /
on request" swatch use a `conic-gradient` and an overlaid label.

## 9. Price table
`.price-table > table` with a `.price-note` disclaimer above it (accent tint).
Right column `.price` (accent, bold); `.price.free` for "ZDARMA"/free rows —
that class must use a **dark** success shade (`--c-success-700`), the mid-tone
green fails WCAG AA on white.

Never invent prices — and never ship `od XX €` either; visitors read it as a
broken page. Bind each cell to config with a neutral public fallback:

```html
<td class="price" data-mh="pricing.exteriorBlinds">Na vyžiadanie</td>
<td class="price free" data-mh="pricing.install">Zameranie ZDARMA</td>
```

`main.js` skips empty config values, so the fallback shows until the owner fills
`pricing.exteriorBlinds: "od 149 € / m²"` in `config.js`. The site is
publishable before prices exist, and updating them is a one-line edit.

## 10. Gallery with filters and "load more"
`.filters[data-gallery-filters]` of `.filter-btn[data-filter="..."]` + a
`.gallery[data-gallery]` of `.tile[data-category="..."]` figures. `gallery.js`
(reused) filters by category **and** reveals tiles in batches of `STEP` (9), so a
30+ photo gallery doesn't dump everything at once. Add the button after the grid
— `gallery.js` hides it automatically when nothing is left to show:

```html
<div class="gallery" data-gallery> …figures… </div>
<div class="text-center mt-2">
  <button class="btn btn--secondary" data-gallery-more>{{Zobraziť viac}}</button>
</div>
```

Only include filter buttons for categories that actually have items, and make
sure `is-hidden` is `display:none` so hidden tiles cost nothing. Changing the
filter resets the batch counter.

## 11. Contact form
`#contact-form` (powered by `form.js`). Fields typically: name, phone, email,
city, product `<select>`, message `<textarea>`, GDPR consent checkbox
(required), submit. Put the `[data-form-alert]` status box **outside** the
`<form>` but let `form.js` find it via `document.querySelector` (see pitfalls —
this bit us once). Associate every `<label for>` with its input; mark required
fields; add `autocomplete`.

## 12. Real photos with fallback
Reference the future real filename and fall back to the placeholder so nothing
looks broken before upload; the real photo appears automatically once added:
```html
<img decoding="async" loading="lazy" width="800" height="600"
     src="assets/img/realizacia-roleta.jpg"
     onerror="this.onerror=null;this.src='assets/img/product-rolety.svg'"
     alt="{{popisná alt}}">
```
For gallery/card tiles the container enforces a 4:3 box (`aspect-ratio` +
`object-fit:cover`), so any photo aspect ratio crops cleanly.

Once the photos are final, `scripts/to_webp.py` wraps each one for WebP delivery.
The `<img>` (with its `onerror`, sizes and lazy-loading) stays untouched inside:

```html
<picture>
  <source srcset="assets/img/realizacia-roleta.webp" type="image/webp">
  <img decoding="async" loading="lazy" width="800" height="600" … >
</picture>
```

This needs `picture { display: contents; }` in the CSS (already in the engine),
otherwise the wrapper becomes a layout box and `height:100%` rules inside tiles
resolve against it instead of the tile.

## 13. Footer + cookie bar + mobile CTA
- `.site-footer` (dark): brand blurb + `[data-mh-social]`, quick links, and a
  `.footer-contact` block bound to config (`data-mh`, `data-mh-tel/-mail`).
- `.cookie-bar#cookie-bar` with `[data-cookie-accept]`/`[data-cookie-decline]`.
- `.mobile-cta` (fixed bottom bar, phone + CTA) shown ≤640px.

Copy all three verbatim from a built site — they're identical everywhere and
wired to `main.js`.

## 14. Rating / social-proof panel (HONEST)
Only real numbers. Bind the rating to `config.reviews.rating` and link to the
real Google profile:
```html
<a class="google-rating" data-mh-href="social.googleReviews" target="_blank" rel="noopener">
  <div class="google-rating__score">
    <span class="big" data-mh="reviews.rating">4,9</span>
    <div><span class="stars">★★★★★</span><small>{{priemer z Google}}</small></div>
  </div>
  <div class="google-rating__cta"><p>{{...}}</p><span class="btn btn--primary">{{Čítať recenzie}}</span></div>
</a>
```
Get a clean Google link from the listing's CID: from a Maps URL take the hex
after the second `0x` in `!1s0x...:0x<CID_HEX>`, convert to decimal, and use
`https://www.google.com/maps?cid=<decimal>`. Keyless map embed for the contact
page: `https://maps.google.com/maps?q=<lat>,<lng>&z=16&output=embed`.
