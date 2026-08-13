---
name: local-business-website
description: >-
  Build a complete, publish-ready marketing / lead-generation website for a
  local business or service (tradesperson, dentist, café, cleaning company,
  small B2B, etc.) from a brief. Produces a static, no-build, multi-page site —
  hand-written HTML/CSS/vanilla-JS themed to the client's brand — with a
  conversion-focused homepage (hero + inquiry wizard), services, pricing,
  gallery, and a contact page with a working form, plus SEO, GDPR cookie
  consent, a config-driven data layer, branded placeholder imagery, and browser
  verification. Use whenever the user wants to CREATE or BUILD a website, landing
  page, company/presentation/brochure site, "web na kľúč", small-business site,
  or a site to get inquiries/leads — of ANY design or theme — even from just a
  brief/PDF. Also use it to add pages, wire real photos, embed a map, or set up
  forms/analytics on a site built this way. Do NOT use for web apps with
  logins/databases, e-commerce checkouts, CMS (WordPress) work, or single-file
  claude.ai artifacts.
---

# Local-business / lead-gen website builder

This skill captures a proven, repeatable pipeline for turning a brief into a
complete, publish-ready website that a non-technical owner can maintain. It is
**design-agnostic**: the same architecture powers wildly different brands — you
re-theme it, you don't rebuild it.

## Why this architecture (read before deviating)

The default is a **static, no-build, multi-page site** (plain HTML + one CSS
file + a few vanilla-JS files). This is a deliberate choice, not laziness:

- **Publishable anywhere, instantly** — drop the folder on Netlify, GitHub
  Pages, or any FTP host. No Node, no build, no server, nothing to break.
- **The owner can actually maintain it** — editing HTML/text or one `config.js`
  is realistic for a small-business owner; a React/CMS build is not.
- **Longevity & speed** — no dependencies to rot, no build to fail; trivially
  hits high PageSpeed scores because there are no frameworks or web fonts.

Deviate only when the brief genuinely needs it: logins/accounts, a database,
real e-commerce checkout, or dozens of frequently-changing content items (then
a static-site generator or CMS is warranted). A "modern look", animations, or a
few dozen pages are **not** reasons to abandon static.

## The data layer that makes it maintainable

All data that appears in many places (phone, e-mail, address, hours, coverage
area, analytics IDs, form key, map, social, review rating) lives in **one**
file, `js/config.js`. `main.js` binds it into the HTML through attributes:

- `data-mh="business.phone"` → sets the element's text
- `data-mh-tel` / `data-mh-mail` → sets `tel:` / `mailto:` href
- `data-mh-href="social.googleReviews"` → sets href from config
- `data-mh-hours`, `data-mh-coverage`, `data-mh-map`, `data-mh-social` → rendered lists/blocks

Page-specific content (product copy, RAL/colour swatches, gallery items) lives
directly in the HTML where it's shown once — **one source of truth**,
SEO-friendly, visible without JS. Don't duplicate content into config.

Two details that repeatedly bite:

- **Registered office ≠ the place customers visit.** Keep both:
  `business.address` (register/invoicing/GDPR) and `business.showroom`
  (premises). The footer, contact page and JSON-LD `address` must use the
  **showroom** so they match the map and the Google profile; invoicing details
  and the GDPR controller paragraph use the **registered office**. Ask the owner
  which is which — the brief usually lists only the registered one.
- **Values the owner still owes you** (prices above all): bind them *and* leave a
  public fallback in the HTML — `<td data-mh="pricing.blinds">Na vyžiadanie</td>`.
  `main.js` ignores empty config values, so the site is publishable today and
  becomes exact the moment the owner types a number. Never ship `od XX €`.

The bundled `assets/engine/` files are the proven implementation of all of the
above. **Start every project by copying them in** — don't rewrite them:

```
assets/engine/config.js  → js/config.js     (fill from brief)
assets/engine/main.js    → js/main.js        (reuse as-is)
assets/engine/wizard.js  → js/wizard.js      (reuse as-is)
assets/engine/form.js    → js/form.js        (reuse as-is)
assets/engine/gallery.js → js/gallery.js     (reuse as-is)
assets/engine/styles.css → css/styles.css    (RE-THEME via :root tokens)
assets/engine/favicon.svg→ assets/favicon.svg (redraw for the brand)
```

## Workflow (phases)

Track these with your todo tool; they run roughly in order but iterate freely.

### 1. Intake — turn the brief into a spec
`references/brief-template.md` is the intake questionnaire this pipeline wants.
Hand it to a client who hasn't written a brief yet; when a brief already exists,
read it **against** that template and note which fields are missing — those gaps
are what causes rework later. Ask for the blocking ones (phone, e-mail, premises
address, legal name + ID, form delivery) before building, not after.

- If the brief is a PDF/DOCX, extract it (use the `pdf` / `docx` skills). If
  `pdftoppm`/pypdf fail on `_cffi_backend`, run `pip install --force-reinstall cffi`.
- Pull out and write down: legal + short business name, domain, ID numbers,
  address, phone, e-mail, hours, service area; **brand colours**; information
  architecture (page list); the actual **copywriting** for each page; and any
  special features (comparison tables, swatches, price tables, wizard steps,
  map, reviews). A good brief already contains the copy — use it verbatim.
- Note the site's **language** — all UI text, comments, and the README go in
  the client's language, not English.

### 2. Scaffold — engine first, tokens first
- Copy `assets/engine/*` into place (table above).
- Open `css/styles.css` and set the brand in the `:root` tokens (`--c-dark`,
  `--c-accent`, `--c-white`, plus derived shades). Re-theming the tokens
  changes the whole site. This is where "different designs/themes" happens —
  colours, radius, font stack, shadows, hero treatment.
- The brand's vivid accent is a **decorative** colour. Text on white and button
  backgrounds carrying white labels use the darker `--c-accent-600`; accent text
  on dark sections uses the lighter `--c-accent-300`. See the token table in
  `references/components.md` — getting this wrong is the most common
  accessibility failure, and re-themed palettes fail it silently.
- Fill `js/config.js` from the brief (leave `⚠ DOPLNIŤ` where the client still
  owes real data — e.g. the real phone number).

### 3. Build pages from the copy
Standard set (rename per brief): `index.html`, plus service/product, pricing,
about, gallery, contact, a privacy/GDPR page, and `404.html`. Every page shares
the same header, footer, cookie bar, and mobile CTA bar. See
`references/components.md` for the copy-paste component library (header, hero,
3-step wizard, benefit/guarantee cards, comparison table, swatch grid, price
table, gallery+filters, contact form, footer, cookie bar) and the exact
`<head>` block (SEO meta, Open Graph, favicons, JSON-LD).

Conversion essentials on the homepage: a strong hero with two CTAs, the **3-step
inquiry wizard** (higher conversion than a static form), trust/benefit blocks,
an education/"did you know" stat block, social proof, and a closing CTA band.

### 4. Imagery
- Generate branded **placeholder** images so the site looks complete before the
  client sends photos: `python scripts/gen_placeholder_svgs.py` (SVG, brand
  colours, self-contained). See its `--help`.
- Render the **raster** OG image (1200×630 PNG) and favicons from SVG with
  `node scripts/render_raster.js` — social platforms won't render SVG previews.
- When the client sends **real photos**, run `python scripts/optimize_photos.py`
  (fixes EXIF rotation, strips metadata, resizes, recompresses) and, if they
  used generic names, pass `--rename map.json` to give SEO-friendly filenames.
  Wire photos in with an `onerror` fallback so nothing ever looks broken before
  upload — see `references/components.md`.
- Once photos are final, add WebP: `python scripts/to_webp.py --dir assets/img
  --wrap-html .` writes `.webp` siblings and wraps each `<img>` in `<picture>`
  (typically −35 % bytes; old browsers still get the JPEG). It is idempotent.
- **A supplied logo is usually a low-res JPEG/PNG.** Don't paste it into the
  header — vectorise it: trace with `vtracer` (`--mode polygon --color_precision 8`),
  then hand-clean the SVG and sample the real brand hex values out of the
  original to seed the `:root` tokens. Produce `logo-mark.svg` (icon) plus
  **dark and light wordmarks** (`.brand__word`) — the footer is dark, the header
  is light, and one wordmark cannot serve both.
- **Sorting a pile of client photos:** build a contact sheet with Pillow and
  *look* at it, then categorise, spot duplicates of photos already on the site,
  and write a rename map. Ask before deleting anything the owner uploaded.

### 5. SEO, legal, performance, accessibility
Details in `references/seo-legal-perf.md`. The must-haves:
- Localised `<title>`/`meta description` per page; `sitemap.xml`; `robots.txt`;
  LocalBusiness JSON-LD on the homepage; canonical URLs; Open Graph + Twitter.
  The JSON-LD block is **static** — `main.js` does not fill it from `config.js`,
  so its `telephone`/`email`/`address` must be edited by hand whenever those
  change, or Google reads a stale contact. `audit_html.py` WARNs on the mismatch
  (pitfall 29). Do **not** put a fabricated `aggregateRating` in it — show the
  real rating in the visible page and link it to the Google profile instead.
- **GDPR cookie consent** bar; analytics (GA4/GTM) load **only after consent**
  (already implemented in `main.js`).
- Performance: `preload` CSS + hero image, `fetchpriority="high"` on the LCP
  image, `decoding="async"` + `loading="lazy"` on images, explicit
  `width`/`height` to avoid layout shift.
- Accessibility: one `<h1>` per page, a "skip to content" link, keyboard-usable
  nav, `prefers-reduced-motion` respected.

### 6. Verify in a real browser (do not skip)
Run `node scripts/verify_site.js --root . --ignore '\.jpg$'` (ignore the photo
names that intentionally 404 before upload). It serves the site, loads every
page, and fails on JS errors, broken internal links/assets, missing a11y
basics, or a non-working mobile menu — then screenshots every page for a visual
pass. **Look at the screenshots.** Read `references/pitfalls.md` for the
specific bugs this catches (they are subtle and easy to reintroduce).

### 7. Final audit — assume the site is still wrong
`verify_site.js` passing means the site *runs*. It does not mean it is correct.
Every bug in part 2 of `references/pitfalls.md` was found on a site that had
already passed it and looked perfect in screenshots. Run all three, and fix what
they report:

```
python scripts/bump_assets_version.py        # ?v= musí sedieť s obsahom css/js
python scripts/audit_html.py    --root .     # zdrojový kód: odkazy, kotvy, data-mh, SEO, zástupné texty
node   scripts/audit_browser.js --root .     # vykreslené: pretečenie, kontrast, dotykové plochy
node   scripts/verify_site.js   --root .     # beh: chyby JS, assety, mobilné menu
```

Then do the two passes no script can do:

- **Trace every number, brand and claim** on the site back to the brief or to
  something the owner confirmed — installation counts, years, ratings, response
  times, *and* product brands/models/suppliers and performance claims. Vague in
  the brief ⇒ vague on the site; not in the brief ⇒ generic, not invented
  (pitfalls 27–28).
- **Read the pages as a customer.** Any sentence that addresses the *owner*
  ("fill this in", "sample template", "see README") is a bug; owner instructions
  belong only in `README.md`.

### 8. Deliver
- Write a `README.md` **in the client's language** explaining how to edit
  common things (via `config.js`), add photos, set up form delivery
  (Web3Forms), analytics, the map, and how to deploy (Netlify / GitHub Pages /
  FTP), plus a pre-launch checklist.
- Add `.nojekyll` (GitHub Pages), a `netlify.toml` (headers + 404 + caching),
  `site.webmanifest`, `.gitignore`.
- **Cache-bust every local CSS/JS reference.** Run
  `python scripts/bump_assets_version.py` — it sets `?v=` to a hash of the CSS/JS
  contents, so the version changes exactly when the files do. Run it **before
  every push that touched `css/` or `js/`**; a date you have to remember to bump
  is a rule you will break (pitfall 14 — and it was broken again *after* being
  written down, which is why this is a script now). `audit_html.py` fails the
  build when the version no longer matches the content.
- Commit and push. If the client pushes their own commits (photo uploads etc.),
  `git fetch` + `git rebase` onto their work rather than clobbering it.
- Hand over a short list of **what only the owner can supply** (real phone,
  prices, form key, analytics ID) and say plainly which of them block launch.

## Core principles (these are what make the result trustworthy)

- **Never fabricate social proof.** Do not invent customer testimonials, names,
  star counts, or review numbers. If you can't obtain real reviews (Google Maps
  is JS-rendered and usually un-scrapeable), show the *real* aggregate rating
  the owner gives you, link it to their Google profile, and ask them to paste
  real quotes. A believable fake review is still a fake review.
- **Real business facts only.** Use exact address/ID/phone from the brief; where
  a real value is still missing, leave a clearly-marked placeholder — never a
  plausible-looking invention.
- **Every number must be traceable.** Install counts, years in business,
  percentages, response times: each one comes from the brief or from the owner.
  If the brief says "hundreds", the site says "hundreds" — turning that into
  "500+" because it reads better is fabrication, and it's the failure mode you
  are most likely to commit without noticing.
- **Product specifics are facts too — don't invent them.** Brands, model/series
  names, named suppliers ("Somfy motors", "rad ISOLINE", "lamela Z-90"), material
  specs, lifespans and performance claims are exactly what an LLM confabulates
  convincingly. Name a brand only if the owner did; otherwise describe generically
  ("motorické ovládanie", "profil v tvare Z / C"). Keep benefit claims to
  defensible "up to" figures and don't assert product physics you don't know —
  an exterior blind's job is summer solar gain, *not* winter heating savings; most
  shading lasts "dlhé roky", not "desiatky rokov". Cut a claim rather than guess.
  (Pitfalls 27–28.)
- **Nothing owner-facing on a public page.** "Fill in the prices", "sample
  template", "see README", `od XX €` — all of it belongs in `README.md`. When a
  value is unknown, show the customer a neutral phrase ("Na vyžiadanie"), never
  scaffolding.
- **Config-driven & no-build** — keep cross-cutting data in `config.js`; keep
  the site buildless so the owner can host and edit it anywhere.
- **Honest imagery** — never lift other people's photos (e.g. reviewers' photos
  from Google) onto the site; use the client's own or clearly-branded
  placeholders. **Caption each photo for what it actually shows** — open it and
  identify the product before you label it or assign a gallery category; look-alike
  categories (exterior blind shot from inside vs. interior blind) are mislabelled
  easily, and a photo reused in two places must be right in both. (Pitfall 26.)
- **Client's language everywhere** the owner or their visitors will read.

## Reference files (load as needed)
- `references/brief-template.md` — client intake questionnaire; also the checklist
  to read an existing brief against, to spot what it doesn't say.
- `references/components.md` — copy-paste HTML/CSS component library + the exact `<head>`.
- `references/seo-legal-perf.md` — SEO, JSON-LD, GDPR/cookies, performance, deploy files.
- `references/pitfalls.md` — concrete bugs from real builds and how to avoid them.

## Bundled slash commands

Because "build me a website" is a task the model often just does directly, this
skill can under-trigger on its own. Two bundled commands cover both entry points:

- **`assets/commands/build-web.md`** (+ Slovak alias `postav-web.md`) — for when
  the brief already exists. Typing `/build-web <brief>` invokes this skill
  explicitly and passes the brief as arguments, with no reliance on
  auto-triggering.
- **`assets/commands/PROMPTsablonaweb.md`** — for when it doesn't. It interviews
  the client through the fields in `references/brief-template.md`, six topic
  rounds rather than field-by-field, then assembles the finished brief and offers
  to start the build. Point it at an existing brief and it fills what it can and
  asks only about the gaps.

To install per project: copy into the repo's `.claude/commands/`. To install
globally (all projects): copy into `~/.claude/commands/`. The user can always
also invoke the skill by name ("use the local-business-website skill").

## Bundled scripts
Build:
- `scripts/gen_placeholder_svgs.py` — branded SVG placeholders (hero, cards, OG).
- `scripts/render_raster.js` — SVG → PNG (OG 1200×630 + favicons) via Chromium.
- `scripts/optimize_photos.py` — EXIF-fix, strip, resize, recompress, rename.
- `scripts/to_webp.py` — WebP siblings + idempotent `<picture>` wrapping (−35 %).
- `scripts/bump_assets_version.py` — sets `?v=` from a hash of css/js content
  (`--check` only reports). Run before any push touching `css/` or `js/`.

Check (all three before delivery):
- `scripts/verify_site.js` — runtime: JS errors, broken assets, mobile menu, screenshots.
- `scripts/audit_html.py` — source: links, anchors, duplicate ids, unresolved
  `data-mh` paths, SEO meta, and **placeholder text leaking to visitors**.
- `scripts/audit_browser.js` — rendered: horizontal overflow (names the culprit),
  WCAG contrast, 24 px tap targets, unfilled data.

Each takes `--root .` and `--help`; the audits exit non-zero on real problems, so
they can gate a delivery. They are deliberately quiet about known non-issues
(text over gradients, inline links, `aria-hidden` decoration) — a checker that
cries wolf gets ignored, and then the real bug ships.

### What each script needs — and what to do when it isn't there
The site itself has **no dependencies**; only the tooling does. Check what's
available before planning the build, and degrade gracefully rather than skipping
verification silently:

| script | needs | if unavailable |
|---|---|---|
| `audit_html.py` | Python stdlib only | always runs — never skip it |
| `optimize_photos.py`, `to_webp.py` | Pillow | `pip install pillow`; if truly impossible, ship the originals and say so |
| `gen_placeholder_svgs.py` | Python stdlib only | always runs |
| `verify_site.js`, `audit_browser.js`, `render_raster.js` | `playwright-core` + Chromium | see below |
| logo tracing | `vtracer` | trace by hand or ask the client for a vector logo |

Chromium is present in Claude Code sandboxes (`/opt/pw-browsers`) but **not in
every environment** — a plain chat sandbox usually has Python but no browser.
Without it you lose the rendered checks (overflow, contrast, tap targets, OG
raster). Then: run `audit_html.py`, re-read the pages as a customer, check the
contrast of your palette numerically against the token table in
`references/components.md`, and **tell the user which checks you could not run**
— don't present the site as verified.
