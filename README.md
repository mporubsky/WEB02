# BABYLAND — web centra

Nový web pre **1. súkromné opatrovateľské centrum BABYLAND**. Nahrádza pôvodný
web z roku 2004 (rámce, generované z Wordu). Obsah je prevzatý z pôvodného webu,
prepísaný do modernej podoby a doplnený o formuláre, mapu a súhlas s cookies.

Web je **statický** — žiadny WordPress, žiadna databáza, žiadne zostavovanie
(build). Sú to obyčajné HTML súbory, ktoré sa dajú nahrať kamkoľvek a otvoriť
aj priamo z disku. Vďaka tomu je rýchly, lacný na prevádzku a nič sa na ňom
nemá ako pokaziť.

---

## ⚠ Čo treba doplniť pred spustením

Toto sú jediné veci, ktoré neviem doplniť za vás. Prvé tri **blokujú spustenie**,
zvyšok je vylepšenie.

| # | Čo | Kde to zmeniť | Blokuje spustenie? |
|---|---|---|---|
| 1 | **Overiť telefón** `0908 41 40 91` — je z webu z roku 2004 | `js/config.js` → `business.phone` a `phoneHref` | **Áno** |
| 2 | **Overiť adresu prevádzky** `Nobelovo nám. 6, Bratislava` + doplniť PSČ | `js/config.js` → `business.showroom` | **Áno** |
| 3 | **Kľúč na doručovanie formulárov** (Web3Forms, zdarma) | `js/config.js` → `form.web3formsKey` | **Áno** – bez neho sa formulár odošle cez e-mailový program |
| 4 | **Vlastné fotky** — teraz sú tam 4 fotky zachránené z pôvodného webu (majú len 342 px, sú zrnité) | `assets/img/` | Nie, ale veľmi odporúčam |
| 5 | Odkaz na Facebook / Google profil | `js/config.js` → `social` | Nie |
| 6 | Merací kód Google Analytics | `js/config.js` → `analytics.ga4Id` | Nie |

Miesta na doplnenie sú v `js/config.js` označené `⚠ DOPLNIŤ`.

**Cenník web zámerne nemá.** Pôvodný web ho nemal a jediná cena, ktorá na ňom
bola (`1750 Sk za 10 stretnutí` pri sobotných dopoludniach), je v korunách
a dávno neplatí. Vymyslieť ceny nejde. Ak cenník chcete, dajte mi vedieť sumy
a stránku doplním.

**Ešte si prosím prejdite otváracie hodiny.** Pôvodný web ich uvádzal dvakrát
a zakaždým inak — slovenská stránka `7:00 – 17:00` (predĺžene `6:00 – 19:00`),
anglická `8 a.m. – 3 p.m.`. Použil som slovenskú verziu; ak platí iná, zmeňte ju
v `js/config.js` → `business.hours`.

---

## Ako web upraviť

### Bežné údaje — všetko v jednom súbore

Telefón, e-mail, adresa, otváracie hodiny, mapa, sociálne siete a merací
kód sú **len na jednom mieste**: `js/config.js`. Keď ich tam zmeníte, prepíšu sa
automaticky na všetkých stránkach.

Príklad — zmena telefónneho čísla:

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

### Texty na stránkach

Texty sú priamo v HTML súboroch — otvorte príslušný súbor v textovom editore
a prepíšte, čo treba. Sú to obyčajné súbory, netreba nič inštalovať.

| Súbor | Stránka |
|---|---|
| `index.html` | Úvodná stránka |
| `sluzby.html` | Opatera detí |
| `kurzy.html` | Jazykové kurzy |
| `o-nas.html` | O nás a filozofia |
| `galeria.html` | Galéria |
| `kontakt.html` | Kontakt |
| `en.html` | Anglická stránka |
| `ochrana-osobnych-udajov.html` | GDPR |
| `404.html` | Stránka pri chybnom odkaze |

**Hlavička a pätička sú v každom súbore zvlášť.** Keď ich meníte, zmeňte ich
rovnako vo všetkých — inak sa stránky začnú od seba líšiť.

### Fotky

Fotky patria do priečinka `assets/img/`. Odporúčaná šírka je 1600 px, formát JPG.

Kde sa dajú vymeniť zástupné obrázky za skutočné fotky:

| Kde | Súbor a riadok | Teraz tam je |
|---|---|---|
| Veľká fotka na úvode | `index.html`, hľadajte `hero.svg` | zástupný obrázok |
| Karta „Celodenná opatera" | `index.html`, `sluzba-celodenna.svg` | zástupný obrázok |
| Karta „Poldenná a hodinová" | `index.html`, `sluzba-poldenna.svg` | zástupný obrázok |
| Karta „Jazykové kurzy" | `index.html`, `kurzy-jazyky.svg` | zástupný obrázok |

Postup: fotku uložte do `assets/img/`, v HTML nahraďte cestu k `.svg` cestou
k vašej fotke a **doplňte popis do `alt=""`** (napr.
`alt="Deti pri rannom kruhu v herni"`) — číta ho Google aj nevidiaci návštevníci.

Skutočné fotky (z pôvodného webu) sú v galérii:
`herna-interier-hracky.jpg`, `deti-hra-plysovy-medved.jpg`,
`vytvarne-aktivity-stol.jpg`, `deti-pieskovisko-vonku.jpg`.

> Ak fotky obsahujú tváre detí, potrebujete **súhlas rodičov** so zverejnením.
> Pôvodné štyri fotky boli verejne na starom webe, ale súhlasy si prosím overte.

### Doručovanie formulárov (Web3Forms — zdarma)

Bez nastavenia sa formulár odošle cez e-mailový program návštevníka. Aby chodil
priamo do vašej schránky:

1. Choďte na <https://web3forms.com>
2. Zadajte e-mail `info@babyland-centrum.sk` — príde vám **Access Key**
3. Vložte ho do `js/config.js`:
   ```js
   form: { web3formsKey: "sem-vlozte-kluc" }
   ```
4. Spustite `bump_assets_version.py` (viď vyššie) a otestujte odoslaním dopytu.

### Mapa

Mapa sa vyhľadáva podľa adresy prevádzky a **nepotrebuje žiadny API kľúč**.
Ak by ukazovala nepresné miesto, v `js/config.js` nahraďte adresu súradnicami:

```js
maps: { embedSrc: "https://maps.google.com/maps?q=48.1234,17.1050&z=16&output=embed" }
```

### Meranie návštevnosti

Do `js/config.js` → `analytics.ga4Id` vložte kód `G-XXXXXXXXXX` z Google
Analytics. Meranie sa spustí **až potom, ako návštevník klikne „Súhlasím"**
v lište o cookies — tak to vyžaduje GDPR. Bez súhlasu sa nenačíta nič.

---

## Zverejnenie webu

Ktorýkoľvek z týchto spôsobov, stačí si vybrať jeden:

**1. Netlify (najjednoduchšie, zdarma)** — na <https://app.netlify.com/drop>
pretiahnite celý priečinok. Súbor `netlify.toml` sa použije automaticky.
Vlastnú doménu nastavíte v *Domain settings*.

**2. GitHub Pages** — *Settings → Pages*, vyberte vetvu a `/ (root)`. Pre vlastnú
doménu pridajte súbor `CNAME` s obsahom `www.babyland-centrum.sk`.
Súbor `.nojekyll` už v projekte je.

**3. Klasický hosting cez FTP** — nahrajte celý obsah priečinka do `public_html`
alebo `www`.

> Po aktualizácii môže prehliadač ešte chvíľu ukazovať starú verziu. Pomôže
> **Ctrl+F5** (na Macu Cmd+Shift+R). Rôzne stránky sa môžu obnoviť s malým
> časovým odstupom — nie je to chyba, je to len dočasné ukladanie do pamäte.

---

## Kontrola pred spustením

- [ ] Telefónne číslo je aktuálne a dá sa naň dovolať
- [ ] Adresa prevádzky sedí a mapa ukazuje správne miesto
- [ ] Doplnené PSČ prevádzky
- [ ] Formulár na `kontakt.html` naozaj doručí správu (skúšobné odoslanie)
- [ ] Otváracie hodiny sú aktuálne
- [ ] Fotky sú vaše a máte súhlas rodičov na zverejnenie tvárí detí
- [ ] Text na `ochrana-osobnych-udajov.html` prešiel právnou kontrolou
- [ ] Doména smeruje na nový web

> **Ochrana osobných údajov:** stránku som pripravil na základe toho, čo web
> reálne zbiera (kontaktný formulár a cookies). **Nie som právnik** — pred
> spustením ju dajte skontrolovať niekomu, kto sa GDPR venuje, hlavne časť
> o dobe uchovávania údajov.

---

## Pre technikov

Statické HTML + jeden CSS súbor + niekoľko súborov vanilla JS. Žiadne závislosti,
žiadny build.

```
index.html …            stránky
css/styles.css          celý dizajn; značkové farby sú v :root na začiatku
js/config.js            údaje firmy (jediný súbor na bežné zmeny)
js/main.js              napĺňanie data-mh, menu, cookies, mapa, reveal
js/wizard.js            3-krokový dopytový sprievodca na úvodnej stránke
js/form.js              kontaktný formulár
js/gallery.js           filtre galérie
assets/img/             obrázky (skutočné fotky + zástupné SVG)
```

Prefarbenie značky = zmena premenných v `:root` v `css/styles.css`.
Pozor na kontrast: `--c-accent` (limetková) je **len dekoratívna**; pre text
a tlačidlá s bielym popisom používajte `--c-accent-600`.

Kontrolné skripty (v `.claude/skills/local-business-website/scripts/`):

```bash
python3 scripts/bump_assets_version.py     # ?v= podľa obsahu css/js — po každej zmene
python3 scripts/audit_html.py    --root .  # odkazy, kotvy, SEO, zástupné texty
node    scripts/audit_browser.js --root .  # pretečenie, kontrast, dotykové plochy
node    scripts/verify_site.js   --root .  # chyby JS, assety, mobilné menu + snímky
```

Skripty v prehliadači potrebujú `playwright-core` a Chromium; `audit_html.py`
a `bump_assets_version.py` vystačia so samotným Pythonom.
