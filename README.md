# BABYLAND — web centra

Moderná verzia pôvodného webu **babyland-centrum.sk** (2004, rámce generované
z Wordu). Obsah je prevzatý z pôvodného webu — texty, štruktúra aj fotografie.
Nič sa nedopĺňalo: web ponúka presne to, čo ponúkal predtým, len v podobe, ktorá
funguje na mobile, dá sa nájsť v Google a dá sa upravovať.

Web je **statický** — žiadny WordPress, žiadna databáza, žiadne zostavovanie
(build). Sú to obyčajné HTML súbory, ktoré sa dajú nahrať kamkoľvek a otvoriť
aj priamo z disku. Vďaka tomu je rýchly, lacný na prevádzku a nič sa na ňom
nemá ako pokaziť.

---

## Štruktúra — zrkadlí pôvodné menu

| Súbor | Stránka | Pôvodný zdroj |
|---|---|---|
| `index.html` | Úvod | `Babyland.htm` + úvodný pozdrav z `Babyland-ponuka.htm` |
| `ponuka.html` | Ponuka | `Babyland-ponuka.htm` (Kde / Kedy / Čo / Kto) |
| `kurzy.html` | Kurzy AJ pre deti | `Kurzy AJ pre deti.htm` + `AktualnaPonuka.htm` |
| `filozofia.html` | Naša filozofia | `NasaFilozofia.htm` + `FILOZOFIA.htm` + `Hra.htm` |
| `na-navsteve.html` | Na návšteve u nás | `NaNavsteve.htm` (4 fotografie) |
| `kontakt.html` | Kontakt | `kontakt-contact.htm` |
| `404.html` | Stránka pri chybnom odkaze | — |

Anglická vetva má vlastnú navigáciu, rovnako ako pôvodný web:

| Súbor | Stránka | Pôvodný zdroj |
|---|---|---|
| `en/index.html` | Kindergarten | `Kindergarten.htm` |
| `en/program.html` | The Kindergarten Program | `The Kindergarten Program.htm` |
| `en/exclusive.html` | Exclusive for Babyland | `Exclusive for babyland.htm` |
| `en/contact.html` | Contact | `kontakt-contact.htm` |

Medzi jazykmi sa prepína odkazom **English** / **Slovensky** v menu.

---

## ⚠ Čo treba overiť pred spustením

Údaje sú prevzaté z webu z roku 2004 — prosím, potvrďte ich.

| # | Čo | Kde to zmeniť | Blokuje spustenie? |
|---|---|---|---|
| 1 | **Telefón** `0908 41 40 91` | `js/config.js` → `business.phone` a `phoneHref` | **Áno** |
| 2 | **Adresa prevádzky** `Nobelovo nám. 6, Bratislava` + doplniť PSČ | `js/config.js` → `business.showroom` | **Áno** |
| 3 | **Otváracie hodiny** | `js/config.js` → `business.hours` | **Áno** |
| 4 | **Vlastné fotky** — teraz sú tam 4 fotky z pôvodného webu (342 px, zrnité) | `assets/img/` | Nie, ale odporúčam |

Miesta na doplnenie sú v `js/config.js` označené `⚠ DOPLNIŤ`.

**Hodiny si prosím prejdite pozorne.** Pôvodný web ich uvádzal dvakrát a zakaždým
inak — slovenská stránka `7:00 – 17:00` (predĺžene `6:00 – 19:00`), anglická
`8 a.m. – 3 p.m.` (s krajnými hodnotami 7 a.m. a 6 p.m.). Použil som slovenskú
verziu na celom webe vrátane anglickej vetvy, aby si stránky neprotirečili.

**Čo som z pôvodného webu nepreniesol:**

- **Cenu `1750 Sk za 10 stretnutí`** (sobotné hravé dopoludnia) — je v korunách
  a dávno neplatí. Cenník web nemá, rovnako ako ho nemal pôvodný.
- **Oznam „Od 1. septembra 2004 aj v nových priestoroch na Fedinovej 7
  v Petržalke"** — potvrdili ste, že platí Nobelovo nám. 6.
- **Mapku z `atlas.sk`** — bol to screenshot cudzej mapy. Nahradil ju odkaz
  „Zobraziť na mape" na kontaktnej stránke.

Ak niečo z toho platí aj dnes, dajte vedieť a doplním to.

---

## Ako web upraviť

### Kontaktné údaje — všetko v jednom súbore

Telefón, e-mail, adresa, otváracie hodiny a odkaz na mapu sú **len na jednom
mieste**: `js/config.js`. Keď ich tam zmeníte, prepíšu sa automaticky na
všetkých stránkach.

```js
business: {
  phone:     "0908 41 40 91",     // ← ako to uvidí návštevník
  phoneHref: "+421908414091",     // ← na čo sa vytočí po kliknutí
}
```

Zmeňte **obe** hodnoty — prvá sa zobrazuje, druhá sa vytáča.

> **Dôležité:** po každej úprave v `js/` alebo `css/` spustite
> `python3 .claude/skills/local-business-website/scripts/bump_assets_version.py`.
> Zmení sa tým `?v=…` v odkazoch na súbory a prehliadače návštevníkov si stiahnu
> novú verziu. Bez toho môžu rodičia týždeň vidieť starý telefón.

> **Pozor na dve výnimky.** Otváracie hodiny na anglických stránkach a blok
> `JSON-LD` na konci `index.html` sa z `config.js` **neplnia** — sú napísané
> priamo v HTML. Ak zmeníte telefón, adresu alebo hodiny, prepíšte ich aj tam.

### Texty

Texty sú priamo v HTML súboroch — otvorte príslušný súbor v textovom editore
a prepíšte, čo treba. Netreba nič inštalovať.

**Hlavička a pätička sú v každom súbore zvlášť.** Keď ich meníte, zmeňte ich
rovnako vo všetkých — inak sa stránky začnú od seba líšiť.

### Fotky

Fotky patria do priečinka `assets/img/`. Odporúčaná šírka je aspoň 1600 px,
formát JPG.

Skutočné fotky z pôvodného webu (stránka *Na návšteve u nás*):
`herna-interier-hracky.jpg`, `deti-hra-plysovy-medved.jpg`,
`vytvarne-aktivity-stol.jpg`, `deti-pieskovisko-vonku.jpg`.

Veľká fotka na úvodnej stránke je zatiaľ **zástupný obrázok**
(`assets/img/hero.svg`). Keď pošlete vlastnú, v `index.html` a `en/index.html`
nahraďte cestu k `hero.svg` cestou k vašej fotke.

Keď pridávate fotku, **vždy doplňte popis do `alt=""`** (napr.
`alt="Deti pri rannom kruhu v herni"`) — číta ho Google aj nevidiaci návštevníci.

> Ak fotky obsahujú tváre detí, potrebujete **súhlas rodičov** so zverejnením.
> Pôvodné štyri fotky boli verejne na starom webe, ale súhlasy si prosím overte.

---

## Čo web zámerne nerobí

Pôvodný web nič z toho nemal, tak to nemá ani nový:

- **žiadny kontaktný formulár** — návštevník zavolá alebo napíše e-mail,
  presne ako to uvádzal pôvodný web;
- **žiadne meranie návštevnosti** a **žiadne cookies** — preto web nepotrebuje
  lištu so súhlasom ani stránku o ochrane osobných údajov;
- **žiadna vložená mapa** — mapa Google by nastavovala cookies tretej strany;
  namiesto nej je odkaz „Zobraziť na mape".

> Ak by ste niekedy chceli formulár alebo Google Analytics, dajte vedieť —
> obe sa dajú doplniť, ale **spolu s nimi bude web potrebovať lištu so súhlasom
> s cookies a stránku o ochrane osobných údajov.**

---

## Zverejnenie webu

**1. Netlify (najjednoduchšie, zdarma)** — na <https://app.netlify.com/drop>
pretiahnite celý priečinok. Súbor `netlify.toml` sa použije automaticky.
Vlastnú doménu nastavíte v *Domain settings*.

**2. GitHub Pages** — *Settings → Pages*, vyberte vetvu a `/ (root)`. Pre vlastnú
doménu pridajte súbor `CNAME` s obsahom `www.babyland-centrum.sk`.
Súbor `.nojekyll` už v projekte je.

**3. Klasický hosting cez FTP** — nahrajte celý obsah priečinka (vrátane
podpriečinka `en/`) do `public_html` alebo `www`.

> Po aktualizácii môže prehliadač ešte chvíľu ukazovať starú verziu. Pomôže
> **Ctrl+F5** (na Macu Cmd+Shift+R). Rôzne stránky sa môžu obnoviť s malým
> časovým odstupom — nie je to chyba, je to len dočasné ukladanie do pamäte.

---

## Kontrola pred spustením

- [ ] Telefónne číslo je aktuálne a dá sa naň dovolať
- [ ] Adresa prevádzky sedí a odkaz „Zobraziť na mape" vedie na správne miesto
- [ ] Doplnené PSČ prevádzky
- [ ] Otváracie hodiny sú aktuálne — v `config.js` aj na anglických stránkach
- [ ] Fotky sú vaše a máte súhlas rodičov na zverejnenie tvárí detí
- [ ] Doména smeruje na nový web

---

## Pre technikov

Statické HTML + jeden CSS súbor + dva súbory vanilla JS. Žiadne závislosti,
žiadny build.

```
index.html …            slovenské stránky
en/                     anglická vetva (vlastná navigácia)
css/styles.css          celý dizajn; značkové farby sú v :root na začiatku
js/config.js            údaje firmy (jediný súbor na bežné zmeny)
js/main.js              napĺňanie data-mh, mobilné menu, tieň hlavičky, reveal
assets/img/             fotografie a zástupné SVG
```

Farby sú prevzaté z **pôvodného loga BABYLAND** — oranžová `#FF9933` je
vzorkovaná priamo z pôvodného nápisu, limetka `#99CC00` z trička postavičky
a žltá `#FFD11A` zo slniečka na starej úvodnej stránke.

Prefarbenie značky = zmena premenných v `:root` v `css/styles.css`.
Pozor na kontrast: `--c-accent` (oranžová) je **len dekoratívna** — biely text
na nej má 2,1 : 1. Pre text a pre tlačidlá s bielym popisom používajte
`--c-accent-600`. Po každom prefarbení prehľadajte repozitár na staré hexy
(`css`, `site.webmanifest`, `<meta name="theme-color">`, SVG v `assets/`)
a spustite `audit_browser.js`.

Kontrolné skripty (v `.claude/skills/local-business-website/scripts/`) —
prehľadávajú aj podpriečinky, takže pokrývajú aj `en/`:

```bash
python3 scripts/bump_assets_version.py     # ?v= podľa obsahu css/js — po každej zmene
python3 scripts/audit_html.py    --root .  # odkazy, kotvy, SEO, zástupné texty
node    scripts/audit_browser.js --root .  # pretečenie, kontrast, dotykové plochy
node    scripts/verify_site.js   --root .  # chyby JS, assety, mobilné menu + snímky
```

`audit_html.py` hlási „chýba cookie lišta“ — je to očakávané, web žiadne
cookies nenastavuje. Skripty v prehliadači potrebujú `playwright-core`
a Chromium; `audit_html.py` a `bump_assets_version.py` vystačia so samotným
Pythonom.
