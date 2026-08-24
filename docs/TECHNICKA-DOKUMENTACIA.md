# Technická dokumentácia

Stav ku commitu, v ktorom bol tento súbor naposledy upravený. Popisuje web
taký, aký naozaj je — nie taký, aký bol plánovaný.

Pre bežné úpravy obsahu pozrite **[PRIRUCKA.md](PRIRUCKA.md)**.

---

## 1. Čo to je

Statický web bez zostavovania (build). Jedenásť HTML súborov, jeden CSS súbor,
dva JS súbory. Žiadny framework, žiadny balíčkovací nástroj, žiadne
`node_modules` v produkcii, žiadna databáza. Web sa dá otvoriť aj priamo
z disku dvojklikom.

| | |
|---|---|
| Stránok | 13 (7 slovenských vrátane 404, 6 anglických) |
| CSS | `css/styles.css`, ~620 riadkov, 18 očíslovaných sekcií |
| JS | `js/main.js` ~276 riadkov, `js/config.js` ~65 riadkov |
| Obrázky | 4 fotografie JPG, 6 vektorov SVG, 4 ikony PNG |
| Externé závislosti za behu | **žiadne** — ani písmo, ani knižnica, ani analytika |

**Prehliadače:** posledné dve verzie Chrome, Edge, Firefox a Safari. Web
používa `clamp()`, `dvh`, `:focus-visible`, `inert` a vlastné CSS premenné.
V staršom prehliadači bude čitateľný, ale bez niektorých vylepšení.

---

## 2. Mapa súborov

```
├── index.html              úvod
├── ponuka.html             Kde / Kedy / Čo / Kto
├── kurzy.html              kurzy angličtiny
├── filozofia.html          filozofia, kvalita, hra
├── na-navsteve.html        galéria štyroch fotiek
├── kontakt.html            kontakt, hodiny, fakturačné údaje
├── 404.html                chybová stránka (noindex)
├── en/                     anglická verzia — preklad slovenskej, generovaná
│   ├── index.html · offer.html · courses.html
│   └── philosophy.html · visit.html · contact.html
├── css/styles.css          jediný štýlový súbor
├── js/
│   ├── config.js           ⭐ údaje o prevádzke — jediné miesto na úpravu
│   └── main.js             logika webu
├── assets/
│   ├── logo-mark.svg       slniečko (hlavička, pätička, favicon)
│   ├── logo-babyland.svg   nápis BABYLAND
│   ├── favicon.svg         to isté ako logo-mark, pre panel prehliadača
│   ├── favicon-32.png · apple-touch-icon.png · icon-192.png · icon-512.png
│   └── img/
│       ├── babyland-kresba.svg   pôvodná kresba centra
│       ├── hero.svg             zástupné pozadie úvodu
│       ├── og-image.svg → .png   náhľad pri zdieľaní odkazu
│       └── 4× fotografia .jpg
├── scripts/kontrola.py     kontrola pravidiel tohto webu
├── docs/                   táto dokumentácia
├── sitemap.xml · robots.txt · site.webmanifest · netlify.toml · .nojekyll
└── .claude/skills/…        skill, z ktorého web vznikol, + audítorské skripty
```

`assets/img/og-image.svg` sa na webe nepoužíva — je to predloha, z ktorej
`render_raster.js` vyrába `og-image.png`. Nemazať.

---

## 2b. Ako vzniká anglická verzia

Anglická verzia **nie je samostatný web**. `scripts/build_site.py` vezme obsah
`<main>` slovenskej stránky, prepíše v ňom texty podľa prekladovej mapy
`TRANSLATE`, prepíše odkazy a cesty k súborom a výsledok zapíše do `en/`.
Štruktúra HTML pritom zostáva nedotknutá — preto obe verzie vyzerajú rovnako
a nemôžu sa rozísť.

```
ponuka.html  ──(<main>)──►  TRANSLATE  ──►  en/offer.html
    │                                            │
    └────── head + header + footer ──────────────┘
              (generuje ten istý skript)
```

Tri veci, ktoré skript rieši a stoja za zapamätanie:

**Preklad sa uplatňuje od najdlhšieho reťazca po najkratší.** „Kde nás
nájdete" je začiatkom vety „Kde nás nájdete, kedy máme otvorené…"; keby sa
uplatnil skôr, rozbil by ju. Vďaka zoradeniu podľa dĺžky nemusí nikto strážiť
poradie v mape.

**Na zalomení riadkov nezáleží.** Kľúč sa hľadá cez `\s+`, takže presunutie
jedného slova na ďalší riadok preklad nerozbije.

**Zvyšky sa hlásia.** Skript po preklade prejde anglický výstup a nájde slová
s písmenami, ktoré angličtina nepozná. Vlastné mená (Gustáva Mallého,
Kamenská…) preskočí. Keď niečo ostane nepreložené, skript to vypíše a skončí
chybou — nedá sa teda ticho zabudnúť na dvojicu v mape.

---

## 3. Ako sa dostanú údaje na stránku

Celá dynamika webu je jeden vzor: **HTML obsahuje zálohu, `config.js` obsahuje
pravdu, `main.js` ich spojí.**

```
js/config.js                 js/main.js                     HTML
──────────────               ──────────                     ────
window.MH_CONFIG   ──────►   applyConfigToPage()   ──────►   [data-mh]
  business.phone             renderOpeningHours()           [data-mh-hours]
  business.hours             fillCurrentYear()              [data-mh-year]
  maps.directLink                                           [data-mh-tel]
                                                            [data-mh-mail]
                                                            [data-mh-href]
```

Kľúčové: **v HTML je vždy aj skutočný text**, nie prázdne miesto:

```html
<span data-mh="business.phone">0908 41 40 91</span>
```

Keď sa `config.js` nenačíta alebo má návštevník vypnutý JavaScript, uvidí
telefón z HTML. Preto sa po zmene v `config.js` musí prepísať aj HTML záloha —
alebo aspoň vedieť, že tam je stará hodnota.

### Podporované atribúty

| Atribút | Čo urobí | Príklad |
|---|---|---|
| `data-mh="cesta"` | nahradí text prvku | `<span data-mh="business.email">` |
| `data-mh-tel` | nastaví `href="tel:…"` | `<a data-mh-tel href="tel:+421…">` |
| `data-mh-mail` | nastaví `href="mailto:…"` | `<a data-mh-mail href="mailto:…">` |
| `data-mh-href="cesta"` | nastaví `href` z configu | `<a data-mh-href="maps.directLink">` |
| `data-mh-hours` | vykreslí tabuľku hodín | `<div class="hours" data-mh-hours>` |
| `data-mh-year` | doplní aktuálny rok | `<span data-mh-year>2026</span>` |

Hodnoty sa vkladajú výhradne cez `textContent` a `setAttribute`, nikdy cez
`innerHTML` — z `config.js` sa teda nedá vložiť HTML ani skript.

### Čo sa z configu **neplní**

Tri miesta sú napísané ručne, a to zámerne:

1. **Otváracie hodiny na anglických stránkach** — `config.js` drží slovenské
   názvy dní.
2. **Blok `application/ld+json`** v `index.html` — číta ho Google ešte
   predtým, než sa spustí JavaScript.
3. **`sitemap.xml`** — statický zoznam adries.

---

## 4. `js/main.js`

IIFE v prísnom režime, bez závislostí. Päť verejných krokov, spúšťajú sa po
`DOMContentLoaded`:

| Funkcia | Čo robí |
|---|---|
| `applyConfigToPage()` | doplní `data-mh…` atribúty |
| `renderOpeningHours()` | vykreslí tabuľku hodín z `business.hours` |
| `fillCurrentYear()` | doplní rok do pätičky |
| `initMobileNav()` | hamburger, `aria-expanded`, `inert`, zameranie |
| `initHeaderShadow()` | trieda `is-scrolled` na hlavičke |

Každá funkcia má v kóde hlavičku s popisom, typmi parametrov, návratovou
hodnotou a príkladom. Každá sa ticho ukončí, keď na stránke nenájde prvok,
ktorý obsluhuje — všetky sa preto dajú spustiť na ktorejkoľvek stránke.

### Dve rozhodnutia, ktoré stoja za vysvetlenie

**Hranica mobilného menu sa nikde nepíše dvakrát.** `initMobileNav()`
nezisťuje šírku okna, ale to, či je hamburger ešte zobrazený
(`getComputedStyle(toggle).display !== "none"`). Keď bola hranica v JS
napísaná ako číslo, po jej posune v CSS sa menu v pásme medzi starou a novou
hodnotou pri zmene veľkosti okna samo zatváralo.

**Pozadie je počas otvoreného menu `inert`.** Bez toho tabulátor prešiel rovno
za prekryv na odkazy, ktoré nebolo vidieť, a čítačky obrazovky ich čítali tiež.
Pri otvorení sa zameranie presunie na prvú položku menu (menu je v HTML pred
hamburgerom, takže tabulátor by z neho viedol mimo), pri zatvorení späť na
hamburger.

---

## 5. `css/styles.css`

Jeden súbor, 18 očíslovaných sekcií — poradie zodpovedá poradiu na stránke.
Zoznam je v komentári na začiatku súboru.

### Farby

Pomenovanie je `--c-<farba>-<číslo>`, kde vyššie číslo znamená tmavší odtieň.
Odtiene `-600` a `-700` sú **overené na kontrast** a smú niesť text; základné
odtiene sú dekoratívne.

| Premenná | Použitie | Kontrast na bielej |
|---|---|---|
| `--c-accent` `#FF9933` | rámy, prúžky, ikony — **nie text** | 2,1 : 1 ❌ |
| `--c-accent-600` `#A85400` | text, tlačidlá | 5,3 : 1 ✅ |
| `--c-accent-700` `#7D3D00` | tlačidlá pri prejdení myšou | 8,3 : 1 ✅ |
| `--c-lime-700` `#4E6B00` | text v zelenej karte | 6,1 : 1 ✅ |
| `--c-sun-700` `#7A5300` | text v žltej karte | 6,9 : 1 ✅ |
| `--c-sky-700` `#0E6E91` | text v modrej karte | 5,7 : 1 ✅ |
| `--c-muted` `#6B584A` | vedľajší text | 6,7 : 1 ✅ |

Karty a odrážky striedajú štyri farby automaticky cez `:nth-child(4n+…)`.
Pri kartách musia byť **oba tvary selektora** — `.grid > .card:nth-child(…)`
aj `.grid > *:nth-child(…) .card` — lebo karta je raz priamym potomkom mriežky
a inokedy je v obale.

### Hranice (media queries)

| Hranica | Čo sa mení |
|---|---|
| 1161 px | menu → hamburger *(premerané: slovenská hlavička potrebuje 1149 px, anglická 1162 px — rozhoduje dlhšia)* |
| 900 px | trojstĺpcová mriežka a galéria → dva stĺpce |
| 880 px | pätička → dva stĺpce |
| 860 px | hero → jeden stĺpec |
| 560 px | mriežky → jeden stĺpec; menšie odsadenie |
| 520 px | galéria a pätička → jeden stĺpec |
| 480 px | telefón v hlavičke → samotná ikona |
| 380 px | menšia značka, podnadpis značky sa skryje |

Hranica 1148 px **nie je okrúhle číslo náhodou**. Slovenská hlavička
(značka + sedem položiek menu + telefón) potrebuje v jednom riadku 1149 px.
Pri nižšej hranici by sa v pásme medzi ňou a 1149 px hlavička nezmestila
a stránka by sa dala posúvať do strany — týkalo by sa to bežných rozlíšení
1024 a 1152 px. **Po zmene počtu položiek menu alebo veľkosti značky treba
hranicu premerať znova.**

### Dve pravidlá, ktoré vyzerajú zvláštne, ale majú dôvod

```css
body { overflow-wrap: break-word; }        /* a NIE overflow-x: hidden */
.tick-list li { overflow-wrap: anywhere; }
```

`overflow-x: hidden` na `body` tu **zámerne nie je**. Predtým tam bol a robil
presne to, čo sa od neho čaká — schoval pretečenie namiesto toho, aby sa
opravilo. Vďaka nemu prešiel audítorský skript ako čistý v čase, keď bolo
tlačidlo hamburgeru na 320 px celé mimo obrazovky.

`.tick-list li` potrebuje `anywhere`, nie `break-word`: položka je flexbox
a jej text je anonymná flex položka s `min-width: auto`. Pri zväčšenom
rozostupe písmen (WCAG 1.4.12) sa `break-word` neuplatní a text vytlačí
stránku do šírky.

---

## 6. Prístupnosť

Overené, nie predpokladané:

- **kontrast** — každá dvojica text/pozadie aspoň 4,5 : 1, čísla vyššie;
- **poradie nadpisov** — `h1` práve raz na stránku, žiadny preskočený stupeň
  (kvôli tomu je nadpis v hero karte `h2` a nadpisy stĺpcov v pätičke tiež `h2`);
- **dotykové plochy** — každý odkaz a tlačidlo aspoň 24 × 24 px (WCAG 2.5.8);
- **zameranie klávesnicou** — viditeľné na každom ovládateľnom prvku;
- **mobilné menu** — pozadie `inert`, zameranie sa presúva dovnútra a späť;
- **rozostupy textu** — pri zväčšení podľa WCAG 1.4.12 sa nič neoreže;
- **jazyk** — `lang` na `<html>`, a `lang="sk"` / `lang="en"` na cudzojazyčných
  vsuvkách, aby ich čítačka vyslovila správne;
- **`prefers-reduced-motion`** — animácie sa vypnú;
- **odkaz „Preskočiť na obsah"** — prvý v poradí tabulátora.

---

## 7. Rýchlosť a cachovanie

Web neťahá zvonku ani jeden bajt: písmo je systémové, ikony sú vložené SVG,
knižnica žiadna.

`netlify.toml` nastavuje na `/assets/*`, `/css/*` a `/js/*` cache na rok
s príznakom `immutable`. Aby sa zmena vôbec prejavila, odkazy v HTML nesú
`?v=<odtlačok obsahu>`, ktorý prepočítava `bump_assets_version.py`.

**Bez spustenia tohto skriptu sa zmena v CSS, JS ani v logu k návštevníkovi
nedostane.** Fotografie `.jpg` sa neverzujú zámerne — pri výmene im treba dať
nový názov súboru.

`netlify.toml` zároveň posiela hlavičky `X-Content-Type-Options`,
`X-Frame-Options`, `Referrer-Policy` a `Permissions-Policy`, a obsahuje
**trvalé presmerovania (301) zo všetkých 14 adries pôvodného webu** — starý web
mal rámce a adresy končiace na `.htm`, takže bez nich by každá záložka a každý
starý výsledok vo vyhľadávači skončil na chybovej stránke. Poradie je dôležité:
zberné pravidlo na 404 musí zostať posledné, lebo Netlify berie prvé pravidlo,
ktoré sedí.

Pri nasadení na GitHub Pages sa `netlify.toml` **neuplatní** — hlavičky,
presmerovania ani chybová stránka nebudú fungovať tak, ako je popísané.

---

## 8. Kontrolné skripty

| Skript | Čo kontroluje | Potrebuje |
|---|---|---|
| `scripts/kontrola.py` | slovenská typografia, poradie nadpisov, opakované odstavce, mŕtve selektory, názov živnosti mimo fakturačných údajov, `alt` a rozmery obrázkov, zhoda hlavičiek a pätičiek naprieč stránkami, zhoda JSON-LD a anglických hodín s `config.js` | Python |
| `scripts/aktualizuj_sitemap.py` | prepíše `sitemap.xml`, dátumy z histórie repozitára | Python + git |
| `scripts/build_site.py` | zostaví všetkých 13 stránok; anglické sú preklad slovenských | Python |
| `.claude/…/audit_html.py` | odkazy, verzie `?v=`, štruktúra `<head>` | Python |
| `.claude/…/audit_browser.js` | kontrast, dotykové plochy, pretečenie | Node + Chromium |
| `.claude/…/verify_site.js` | chyby JS, chýbajúce súbory, snímky | Node + Chromium |
| `scripts/stress_test.js` | pretečenie v troch scenároch (bežne, WCAG 1.4.12 rozostupy, dlhé slovo) na 6 šírkach + zameranie v otvorenom mobilnom menu | Node + Chromium |
| `.claude/…/bump_assets_version.py` | prepočíta `?v=` | Python |

Presné príkazy sú v [PRIRUCKA.md](PRIRUCKA.md), bod 10.

---

## 9. Slabé miesta, o ktorých treba vedieť

Poctivý zoznam toho, čo by sa dalo pokaziť alebo čo raz bude prekážať.

**Hlavička a pätička sú v trinástich kópiách** — ale nepíšu sa ručne.
Generuje ich `scripts/build_site.py`, takže zmena položky menu je jedna úprava
na jednom mieste. `scripts/kontrola.py` navyše porovnáva výsledné hlavičky
a pätičky medzi stránkami a nahlási, ktorý súbor sa vymyká — to zachytí aj
prípad, keď niekto upraví vygenerovaný súbor ručne a zabudne skript spustiť.

**Šírka hlavičky je na hrane.** Anglická hlavička potrebuje 1162 px z 1180 px,
ktoré má obsah k dispozícii (slovenská 1149 px). Dlhší telefón, ôsma položka
menu alebo dlhší názov položky ju pretlačia — vtedy treba premerať hranicu
1161 px znova, a to v OBOCH jazykoch. Postup je popísaný v komentári pri tom
media query.

**Dve miesta s ručne udržiavanými údajmi** (anglické hodiny a JSON-LD) sa môžu
rozísť so `config.js` — `scripts/kontrola.py` ich porovnáva a rozchod nahlási.
Mapa stránok sa už neudržiava ručne, generuje ju `aktualizuj_sitemap.py`.

**Fotografie sú z pôvodného webu, 342 px široké** a po zväčšení zrnité.
Označené sú `width`/`height` podľa skutočnosti, takže layout neskáče, ale
kvalita je vidieť.

**Veľký obrázok na úvode je zástupný** (`hero.svg`), nie skutočná fotka
priestorov.

**Cache na rok je nemilosrdná.** Kto zabudne spustiť `bump_assets_version.py`,
uvidí svoju zmenu, ale návštevníci ešte dlho nie.
