# Pitfalls & gotchas (learned from real builds)

Each is a real bug that shipped or nearly shipped. Format: **symptom → cause → fix.**

## 1. Content invisible when JS is off / blank in screenshots
**Symptom:** whole sections are blank without JavaScript (bad for SEO, no-JS
users) and appear empty in full-page screenshots.
**Cause:** reveal-on-scroll elements start at `opacity:0` and only un-hide via JS.
**Fix:** scope the hidden state to `html.js [data-reveal]` and set the class with
an inline `<script>document.documentElement.className+=" js";</script>` **in
`<head>`** (before the stylesheet, so there's no flash). No JS ⇒ no `.js` class ⇒
content is always visible. Make the reduced-motion override win with
`html.js [data-reveal]{opacity:1!important;transform:none!important}`.

## 2. Form success message never appears
**Symptom:** the form submits (network call fires) but the "thank you" alert
never shows.
**Cause:** the `[data-form-alert]` box sits **outside** `<form>`, but the code
looked it up with `form.querySelector(...)` → `null`.
**Fix:** find it with `document.querySelector('[data-form-alert]')`. (Already
fixed in the bundled `form.js`.) Lesson: query page-level status elements from
`document`, not the form.

## 3. Mobile CTA button shows on desktop / phone number wraps
**Symptom:** two "Book now" buttons on desktop and the header phone breaks onto
several lines.
**Cause:** the in-nav CTA (`.header-mobile-cta`) had no desktop rule, and the
phone had no `nowrap`.
**Fix:** `.header-mobile-cta{display:none}` by default and show it only inside
the mobile menu media query; `.header-phone{white-space:nowrap}`. (Already in
the bundled CSS.)

## 4. Social share preview is blank
**Symptom:** Facebook/LinkedIn/iMessage show no image for the link.
**Cause:** `og:image` pointed at an **SVG**; most platforms only accept raster.
**Fix:** render a 1200×630 **PNG** (`scripts/render_raster.js`) and point
`og:image` at it, with `og:image:width/height/type` set.

## 5. Rastered icons don't match their declared sizes
**Symptom:** `favicon-32.png` is actually 64×64; OG is 2400×1260.
**Cause:** Chromium screenshot with `deviceScaleFactor:2` doubles pixels.
**Fix:** render at `deviceScaleFactor:1`. (The bundled script already does.)

## 6. A Node script won't parse: "Unexpected identifier"
**Symptom:** `node --check` fails inside what looks like a comment.
**Cause:** the sequence `*/` appeared **inside** a `/* … */` block comment (e.g.
writing a glob like `chromium-*/chrome`), closing the comment early.
**Fix:** never write `*/` inside block-comment prose; reword (`chromium-<ver>/…`).

## 7. Screenshots show gray boxes where images should be
**Symptom:** verification screenshots show placeholders/gray instead of images.
**Cause:** (a) below-the-fold `loading="lazy"` images don't load during a
full-page screenshot; (b) reveal elements never `.is-visible` without scrolling.
**Fix (for verification only):** before screenshotting, scroll through the page
to trigger lazy-load AND `document.querySelectorAll('[data-reveal]').forEach(e=>e.classList.add('is-visible'))`.
This is a capture artifact, not a real bug — real users scrolling see them fine.

## 8. `pypdf`/`pdfplumber` crash on `_cffi_backend`
**Symptom:** `ModuleNotFoundError: No module named '_cffi_backend'` when reading
the brief PDF.
**Fix:** `pip install --force-reinstall cffi`, then retry.

## 9. Can't scrape Google reviews
**Symptom:** fetching the Google Maps place URL returns an empty "Google Maps"
shell; a headless browser gets `ERR_CONNECTION_RESET` through the agent proxy.
**Cause:** Maps is JS-rendered and the proxy blocks general browsing.
**Fix:** don't fabricate reviews. Use the **real** rating the owner provides,
link it to their Google profile (via `?cid=`), and ask them to paste real
quotes. See the honesty principle in SKILL.md.

## 10. Find/replace across pages hits the wrong thing
**Symptom:** editing the nav also changed a breadcrumb or an `<h1>`; or removing
a "Home" nav item also removed the breadcrumb "Home" link.
**Cause:** the same text/markup appears in multiple roles (nav vs breadcrumb vs
heading).
**Fix:** scope replacements precisely — match the full anchor
(`<a href="produkty.html">Produkty & služby</a>`), not just the text; when
deleting the nav "Home" item, match the standalone nav line, not the
`<li><a …>Home</a></li>` breadcrumb. Verify with a grep afterwards.

## 11. "The header changes depending on which page section I'm on"
**Symptom:** the client reports different header/markup on different pages after
an update.
**Cause:** GitHub Pages + browser HTTP caching serve stale copies for a few
minutes, and different pages refresh at different times.
**Fix:** it's caching, not code. Hard refresh (Ctrl/Cmd+F5) or wait; confirm the
live HTML with a fetch if unsure. Reassure the client.

## 12. Two sources of truth for content
**Symptom:** prices/swatches drift between `config.js` and the HTML.
**Cause:** putting content that appears once (prices, product copy) into config
as well as the page.
**Fix:** content shown once lives in the HTML (SEO-friendly, no-JS visible).
Only cross-cutting data (phone, email, hours, IDs, analytics, map, rating) lives
in `config.js`.
**Exception — values the owner must fill in later** (prices are the usual case):
bind them with `data-mh` **and** leave a sane public fallback as the HTML text:
`<td data-mh="pricing.blinds">Na vyžiadanie</td>`. `main.js` skips empty config
values, so the fallback stays visible until the owner fills the number in one
place. That is one source of truth per value plus a safe default — not drift.

## 13. Duplicated header/footer drift
**Symptom:** header/footer differ subtly between pages after manual edits.
**Cause:** the header/footer are copied into every page (no build/includes).
**Fix:** when changing shared chrome, edit **all** pages in one scripted pass and
re-run `verify_site.js`. Accept the duplication as the price of no-build
robustness; keep the blocks byte-identical.

---

# Part 2 — found by auditing a finished, already-"done" site

Everything below shipped on a site that had passed `verify_site.js` and looked
perfect in screenshots. They are the reason phase 8 (final audit) exists.

## 14. Client still sees old data after you pushed the fix
**Symptom:** the owner sends a screenshot where the layout is your **new** one
but the phone/address/company name is the **old** value. Looks impossible.
**Cause:** the browser cached `js/config.js`. HTML revalidated, the JS did not —
so new markup got filled with stale data. Hosts serve JS/CSS with long
`max-age`, and this bites hardest right after a data change.
**Fix:** version every local CSS/JS reference —
`<script src="js/config.js?v=20260725">` — and bump the number when you edit
them. Document the bump in the README. Don't tell the client "clear your cache"
as the solution; make it impossible instead.

## 15. Accent text is invisible on a dark hero
**Symptom:** the small "eyebrow" label above the H1 is unreadable (contrast
1.2:1); nobody notices because everyone reads the H1.
**Cause:** `.eyebrow` uses the **dark** accent shade (designed for white
sections), but `.hero` / `.page-hero` have a dark background. Only
`.section--dark` had the light-shade override.
**Fix:** list every dark container in the override:
`.section--dark .eyebrow, .hero .eyebrow, .page-hero .eyebrow, .edu .eyebrow
{ color: var(--c-accent-300); }`. Rule of thumb: after re-theming, check every
token used on **both** light and dark backgrounds.

## 16. The CTA button in the mobile menu has dark, unreadable text
**Symptom:** in the opened mobile menu the primary button shows dark text on the
accent background (1.6:1). Correct on desktop.
**Cause:** CSS specificity. `.main-nav a { color: var(--c-dark) }` (0,1,1) beats
`.btn--primary { color:#fff }` (0,1,0), so the nav wins for a button that is
also a nav link.
**Fix:** re-assert the button inside the nav:
`.main-nav a.btn--primary, .main-nav a.btn--primary:hover { color:#fff; background:var(--c-accent); border-bottom:none; }`
Lesson: whenever a component is nested in a container that styles the same
element type, check the cascade — screenshots of the *closed* menu hide this.

## 17. Page scrolls sideways on a phone because of one button
**Symptom:** a page can be dragged horizontally on a 390 px viewport.
**Cause:** `.btn { white-space: nowrap }` plus a long label and large padding →
the button is wider than the viewport and cannot wrap.
**Fix:** `.btn { max-width:100% }` and, under ~560 px, `white-space: normal` with
smaller `--btn--lg` padding. When hunting overflow, **ignore elements inside
`overflow-x:auto` containers** (a wide table in a scroller is correct) — the
bundled `audit_browser.js` does this and names the real culprit.

## 18. Internal notes and placeholders shipped to the public
**Symptom:** visitors read "prices are placeholders — see `README.md`" on the
pricing page and "this document is a sample template" on the privacy page; the
price column literally says `od XX €`.
**Cause:** scaffolding text written for the owner was never removed, and the
brief's own "placeholder structure" was copied verbatim into a live page.
**Fix:** never address the owner in page copy — owner instructions belong in
`README.md` only. For values that are genuinely unknown, show a neutral public
phrase ("Na vyžiadanie" / "On request"), never `XX`. `audit_html.py` fails the
build on `XX €`, `TODO`, `lorem`, `README.md` and `{{PLACEHOLDER}}` in visible
text — run it before every delivery.

## 19. A specific number nobody can back up
**Symptom:** "500+ successful installations" on the About page. The brief said
"**hundreds** of successful installations".
**Cause:** a vague claim was "improved" into a precise one because specific
numbers read better.
**Fix:** every number on the site must be traceable to the brief or to something
the owner confirmed — installations, years in business, review counts, response
times. If the brief is vague, stay vague ("Stovky"). Grep the finished site for
digits and check each one against the source. This is the same rule as the
never-fabricate-reviews principle, and it is the easiest one to break by accident.

## 20. Registered office vs. the place customers visit
**Symptom:** the footer, contact page and JSON-LD all show the company's
registered address, while the embedded map points somewhere else — and the
owner says "the address is completely wrong".
**Cause:** the brief lists one address (the **registered office**, from the
company register). The place customers actually walk into is often different.
**Fix:** keep both in config (`business.address` = registered office;
`business.showroom` = premises). Use the **showroom** in the footer, on the
contact page and in JSON-LD `address` (it must match the map and the Google
profile); use the **registered office** for invoicing details and the GDPR
controller paragraph. Ask which is which — never guess from the brief alone.

## 21. `site.webmanifest` keeps the old brand colour
**Symptom:** after a re-theme, Android's PWA/tab colour is still the previous
brand colour.
**Cause:** `theme_color` in `site.webmanifest` is a second place the colour
lives; only `<meta name="theme-color">` got updated.
**Fix:** after any re-theme, grep the whole repo for the old hex values —
manifest, meta tags, inline SVG assets, OG image source. They must all agree.

## 22. Wrapping images in `<picture>` breaks the layout
**Symptom:** after adding WebP, gallery tiles collapse or images lose their
aspect ratio.
**Cause:** `<picture>` is a real inline box between the container and the
`<img>`, so rules like `.tile img { height:100% }` now resolve against the
picture, not the tile.
**Fix:** `picture { display: contents; }` — the wrapper stops generating a box
and every existing selector keeps working. (In the bundled CSS.) Also make the
wrapping script **idempotent**: a lookbehind for `<picture>` is not enough
because `<source>` sits between them — test "is this position already inside a
picture element" instead, or a second run will double-wrap every image.

## 23. Tap targets smaller than 24 px
**Symptom:** footer and breadcrumb links are hard to hit on a phone (15–17 px tall).
**Cause:** they are bare inline links with no padding.
**Fix:** `display:inline-flex; align-items:center; min-height:24px` on footer,
breadcrumb and contact links (WCAG 2.5.8). **Do not "fix" links inside a
sentence** — the standard explicitly exempts those, and padding them wrecks the
line spacing.

## 24. A contrast audit that cries wolf
**Symptom:** the checker reports dozens of failures for white text on gradients,
hero overlays and photo captions — all of them fine — and the one real failure
drowns in the noise.
**Cause:** naively walking up for `background-color` returns white when the real
background is a `background-image` (gradient or photo).
**Fix:** while walking the ancestors, note whether any of them sets a
`background-image`. If so, don't report a failure — list the element separately
for a visual check against the screenshots. Report hard failures only for solid
backgrounds, and skip anything inside `aria-hidden="true"` (decorative stars,
icons) because the standard doesn't apply to it.

## 25. A camera watermark on every client photo
**Symptom:** the client says the site "looks cheap" and can't say why. Bottom-left
of every photo reads `REDMI NOTE 9 PRO / AI QUAD CAMERA` — a burned-in phone
watermark. In the gallery the caption gradient half-hides it, so it survives
review; in a hero it sits right under the headline.
**Cause:** many phones ship with the watermark enabled by default. Clients send
photos exactly as the phone saved them.
**Fix:** measure where it starts instead of guessing — sample the bottom band and
find the first row of near-white text pixels (it was at 90 % of height, so cropping
the bottom 12 % cleared it with margin). Then:
- crop **only** the photos that actually have it — check by eye on a contact sheet
  of every photo's bottom-left corner; a few are usually clean and don't need it;
- re-encode the WebP siblings afterwards, or the old watermarked ones keep serving;
- the crop tightens the framing, which usually *improves* these photos (it removes
  foreground paving and dirt).

Same sweep applies to date stamps and "Shot on …" overlays. Check the corners of
client photos before wiring any of them in.

## 26. A photo captioned as the wrong product
**Symptom:** the same photo is used in two places (a homepage product card *and* a
gallery tile) and both call it an **interior** blind — but it is actually an
**exterior** blind shot from inside the room. The owner spots it instantly; you
never would from a thumbnail.
**Cause:** wiring photos by filename/position without identifying what is in each
one. Product categories that look alike at a glance are the trap: an exterior
venetian blind photographed **from inside** (wide slats outside the glass, side
guide wires) reads as "blinds on a window" and gets filed as interior; a fabric
day/night roller vs. aluminium venetian; a conservatory screen vs. an awning.
**Fix:** *look* at every photo before you caption it and before you pick which
category it belongs to — open it, don't trust the filename. A photo reused in
several places must be re-checked in **each** context (a product card asserts a
category; a gallery tile asserts a caption + a `data-category` filter). When you
rename it to reflect reality, rename **both** the `.jpg` and `.webp` and update
every reference. Domain tell-tales worth learning: exterior blinds sit *outside*
the glass and have side guide cables; interior blinds/rollers sit on the sash.
When unsure, ask the owner — the same rule as "seven photos were captioned wrong".

## 27. Invented product brands, model names or suppliers
**Symptom:** the copy names a specific product line ("rad ISOLINE"), a model code
("lamela Z-90 vs C-80") or a component supplier ("motory Somfy") that the brief
never mentioned. It reads as authoritative technical detail — and the owner may
not sell that brand at all, which is a factual claim they can't stand behind.
**Cause:** the same instinct as pitfall 19 (a vague claim "improved" into a
precise one), but for **product specifics**: a plausible-sounding model or brand
makes the page feel expert, so the model supplies one. Model codes and premium
supplier names are exactly what an LLM confabulates convincingly.
**Fix:** treat product brands, model/series names and named suppliers as facts
that must come from the brief or the owner — never invented. Prefer **generic,
verifiable descriptions**: "exteriérové hliníkové žalúzie", "profil v tvare Z /
C" (a real geometric descriptor, not a model code), "motorické ovládanie"
(without naming a motor brand). If the owner confirms a specific brand, use it;
otherwise stay generic. This is the never-fabricate principle extended from
reviews/numbers to the product catalogue itself.

## 28. A benefit that sounds good but is domain-wrong or unprovable
**Symptom:** "exterior blinds save on **winter heating** — an insulating cushion
that pays back all year"; "will last **decades**"; "get a **quote in 30 seconds**".
Each reads well; each is wrong or unsupportable. Exterior shading's real job is
blocking summer solar gain — the winter-heating story is dubious; fabric awnings
and motors last ~10–15 years, not "decades"; the wizard sends an inquiry in 30
seconds, it does not return a price.
**Cause:** AI-generated marketing rounds every product up to the maximum benefit
and invents symmetry ("great in summer *and* winter"), plausible-but-inflated
lifespans, and headlines that promise more than the mechanism delivers.
**Fix:** claims about how a product performs are facts too. Keep quantified
benefits to defensible "up to" figures the owner can source; describe realistic
lifespan ("dlhé roky", not "desiatky rokov"); make the CTA describe what actually
happens ("*Vyžiadajte si* cenovú ponuku za 30 sekúnd", not "*Získajte*"). When you
don't know the physics of the product, don't assert it — cut the claim rather than
guess. Read the finished copy as a skeptical customer and delete anything you
couldn't prove.

## 29. Structured data (JSON-LD) drifts from `config.js`
**Symptom:** the visible phone/e-mail update the moment the owner edits
`config.js`, but Google reads a **different** number — the JSON-LD still has the
old/placeholder value (e.g. `+421900000000`, `info@…placeholder`).
**Cause:** the LocalBusiness JSON-LD block is **static HTML**; `main.js` binds
`config.js` into visible `data-mh` elements but not into the JSON-LD `<script>`.
So the two silently diverge — worst right after the owner fills real contact
details, exactly when it matters for local SEO.
**Fix:** whenever you change contact details in `config.js`, update the JSON-LD
`telephone`/`email`/`address` in the HTML by hand too. `audit_html.py` now WARNs
when JSON-LD `telephone`/`email` doesn't match `config.js` — treat that warning as
a release blocker for launch even though it isn't a hard error. Same class as
pitfall 21 (`site.webmanifest` colour): any value that lives in a second,
non-config place must be kept in sync deliberately.

---

# Part 3 — found by rebuilding a 2004 site and then stress-testing the result

Pitfalls 30–38 all come from one project: modernising an existing kindergarten
site. Every one of them was live in a build that had already passed
`audit_html.py`, `audit_browser.js` **and** `verify_site.js` with green ticks.

## 30. `overflow-x: hidden` on `body` hides your own bugs
**Symptom:** `audit_browser.js` reports "no horizontal overflow" while the
hamburger button is, at 320 px, entirely off the right edge of the screen. The
mobile menu literally cannot be opened, and nothing warns you.
**Cause:** the engine shipped `body { overflow-x: hidden }`. Every overflow
check derives from `documentElement.scrollWidth > innerWidth`, and that rule
makes the symptom unmeasurable. It also breaks `position: sticky` in some
engines and can clip focus outlines.
**Fix:** the engine no longer has it. Use `body { overflow-wrap: break-word }`
so long words wrap instead, and let real overflow show — then fix the cause.
If you ever add `overflow-x: hidden` back, you have disabled your own audit.

## 31. A round-number nav breakpoint that was never measured
**Symptom:** the page scrolls sideways on 1024 px and 1152 px screens — two of
the most common laptop widths — while phones and 1440 px desktops are fine.
**Cause:** the hamburger appeared at ≤ 940 px because 940 is a nice number. The
desktop header (brand + 7 nav items + phone) actually needed **1149 px**. So
between 941 and 1148 px the header was wider than the viewport.
**Fix:** *measure* it. Set the breakpoint to `1px` temporarily so the desktop
header renders at every width, binary-search the narrowest width where
`documentElement.scrollWidth <= innerWidth`, then set the media query one pixel
below it. Do this in the **longest** language the site ships. Re-measure after
any change to the nav item count, the brand, or the phone format — and leave a
comment in the CSS saying the number was measured and what it depends on.
Corollary: check the header still fits inside `--container` (content width),
not merely inside the viewport, or it will sit wider than the rest of the page.

## 32. The same breakpoint written in both CSS and JS
**Symptom:** you move the nav breakpoint in CSS; afterwards, resizing the window
anywhere in the old-to-new range silently closes the open mobile menu.
**Cause:** `main.js` had `if (window.innerWidth > 940) close()`. Two sources of
truth for one number.
**Fix:** the engine now asks the DOM instead:
`window.getComputedStyle(toggle).display !== "none"`. The hamburger's own
visibility *is* the breakpoint. Never copy a media-query value into JS.

## 33. Keyboard focus escapes behind the open mobile menu
**Symptom:** open the menu on a phone, press Tab — focus jumps straight past the
overlay onto links in the page behind it. The menu items are never reached, and
the focus ring is invisible because it is under the overlay.
**Cause:** nothing made the background unreachable, and the nav sits *before*
the toggle in the DOM, so Tab from the toggle leaves the header entirely.
**Fix:** the engine now sets `inert` on every `<body>` child except the header
while the menu is open, moves focus to the first menu link on open, and returns
it to the toggle on close (also on Escape). Guard with
`if ("inert" in HTMLElement.prototype)`. Test it: open the menu, press Tab ten
times, and assert every stop is inside the header or the nav.

## 34. A media query placed above the rule it is meant to override
**Symptom:** `@media (max-width: 380px) { .brand__word { height: 18px } }` has
no effect. Devtools shows it struck through.
**Cause:** it sat *above* the base `.brand__word { height: 20px }`. Same
specificity ⇒ source order decides, and the base rule wins.
**Fix:** put narrow-screen overrides **after** the rules they override. This is
invisible in review and invisible in screenshots at the widths you happen to
test — the only reliable detection is measuring the computed value at the width
the media query targets.

## 35. Heading levels skip, everywhere, by construction
**Symptom:** `h1 → h3` in the hero card and `h2 → h4` in the footer, on every
page.
**Cause:** headings were chosen by how big they should look. The hero card used
`h3` because `h3` is the card size; the footer used `h4` because the columns are
small.
**Fix:** pick the level from the document outline, then style it. The hero card
heading is `h2` with `font-size: var(--fs-500)`; footer column headings are `h2`
with the small footer size. Assert in CI: exactly one `h1` per page, no level
skipped.

## 36. Locale typography: a Slovak site set in English punctuation
**Symptom:** nothing looks broken, but the text reads as translated. On a narrow
phone, single-letter prepositions dangle at the ends of lines all over the page.
**Cause:** the copy used `—` (em dash) and plain spaces. Slovak (STN 01 6910)
has no em dash — the parenthetical dash is `–` — and single-letter prepositions
(a, i, o, u, v, s, z, k) must be bound to the next word with `&nbsp;`.
**Fix:** apply per-locale typography and never globally: the Slovak pages get
`–` and 128 non-breaking spaces; the English pages keep `—` and get none. Two
traps when automating it: apply the dash swap to `alt=`, `<title>` and
`<meta description>` too (a screen reader reads `alt`), and *loop* the
non-breaking-space substitution — one pass fixes only the first of two adjacent
one-letter words ("a s láskou" ⇒ "a&nbsp;s láskou", not "a&nbsp;s&nbsp;láskou").
Also mark foreign phrases with `lang`: an English phrase inside Slovak body copy,
and the Slovak legal name inside English pages, or the screen reader mispronounces
both.

## 37. The old site is not a source of current facts
**Symptom:** the rebuilt site shipped with the wrong street address, the wrong
opening hours, and described the business as something it no longer is.
**Cause:** everything was faithfully carried over from the site being modernised.
That site was twenty years old. Business directories repeated the same stale
address, so they "confirmed" it.
**Fix:** when the job is "modernise this existing site", treat its content as
**copy**, not as **facts**. Before launch, verify against something current —
the Google Maps listing, a photo of the notice on the door, the owner. Check at
minimum: trading name, street address, opening hours, phone, and what the
business actually calls itself. Ask for it explicitly in intake.

## 38. The trade-licence name is not what the business *is*
**Symptom:** the site called itself "1. súkromné opatrovateľské centrum" in the
brand lockup, page titles, `site.webmanifest`, and `ChildCare` structured data.
The place is a kindergarten; that phrase is only part of the sole trader's
registered name.
**Cause:** the legal name from the registry was used as the business
description because it was the longest, most official-looking string available.
**Fix:** separate the two and use each in exactly one place. What the business
*is* goes in the brand descriptor, headings, titles, meta descriptions, the
manifest and `@type`. The registered name goes only in the billing/legal block
and the copyright line. Add a repo check that fails if the registered name
appears anywhere else. (Same family as pitfall 20: registered office vs. the
address customers visit.)

## 39. Tracing a low-resolution logo produces wavy letters
**Symptom:** the vectorised wordmark looks fine at 20 px in the header and
visibly wobbly the moment anyone zooms in — every edge has a slight ripple.
**Cause:** the source was an 87 px-tall GIF. `potrace` faithfully reproduced the
anti-aliasing staircase. Smoothing removes the ripple but deforms the letters
(the counter of "A" turns into a blob).
**Fix:** for a logo, measure and *reconstruct* rather than trace. Read the cap
height, stroke weight and each letter's x-bounds off the bitmap, then build the
glyphs from straight lines and ellipse arcs. Overlay the result on the source to
confirm it stays within 1–2 px. On this project the path went from 23.6 kB of
trace noise to 1.0 kB of clean geometry. Trace only artwork that is genuinely
irregular (a hand drawing), never type.
