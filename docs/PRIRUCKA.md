# Príručka — ako web upraviť

Návod krok za krokom pre bežné úpravy. Netreba programovať ani nič inštalovať:
web sú obyčajné súbory, ktoré otvoríte v textovom editore a prepíšete.

**Odporúčaný editor:** [Visual Studio Code](https://code.visualstudio.com)
(zdarma, Windows aj Mac). Zvýrazní vám kód farebne a upozorní na preklep
v značkách.

---

## Obsah

1. [Zlaté pravidlo: po každej úprave](#1-zlaté-pravidlo-po-každej-úprave)
2. [Zmena telefónu, e-mailu, adresy alebo hodín](#2-zmena-telefónu-e-mailu-adresy-alebo-hodín)
3. [Zmena textu na stránke](#3-zmena-textu-na-stránke)
4. [Výmena alebo pridanie fotky](#4-výmena-alebo-pridanie-fotky)
5. [Pridanie novej stránky do menu](#5-pridanie-novej-stránky-do-menu)
6. [Pridanie položky do zoznamu alebo novej karty](#6-pridanie-položky-do-zoznamu-alebo-novej-karty)
7. [Zmena farieb](#7-zmena-farieb)
8. [Úprava anglickej verzie](#8-úprava-anglickej-verzie)
9. [Pravidlá pre slovenský text](#9-pravidlá-pre-slovenský-text)
10. [Kontrola pred zverejnením](#10-kontrola-pred-zverejnením)
11. [Keď sa niečo pokazí](#11-keď-sa-niečo-pokazí)

---

## 1. Zlaté pravidlo: po každej úprave

Po **každej** úprave spustite v priečinku projektu tieto dva príkazy —
v tomto poradí:

```bash
python3 scripts/build_site.py
python3 .claude/skills/local-business-website/scripts/bump_assets_version.py
```

**Prvý** prestaví stránky: prepíše hlavičku, pätičku a celú anglickú verziu,
aby všetkých trinásť stránok zostalo rovnakých. Bez neho by sa slovenská
a anglická verzia rozišli.

**Druhý** rieši pamäť prehliadača: prehliadače si súbory ukladajú, aby sa web
načítaval rýchlo.
Server im hovorí, že si ich môžu nechať **celý rok**. Skript zmení `?v=…`
v odkazoch na súbory, čím prehliadaču povie „toto je nová verzia, stiahni si
ju znova".

Bez toho môže rodič vidieť starý telefón ešte dlhé mesiace.

> **Fotky (`.jpg`) sa takto neverzujú.** Keď meníte fotku, dajte jej **nový
> názov súboru** — inak ju vracajúci sa návštevník neuvidí.

---

## 2. Zmena telefónu, e-mailu, adresy alebo hodín

Všetky tieto údaje sú **na jedinom mieste**: `js/config.js`. Zmena sa
premietne na všetky slovenské stránky naraz.

**Postup**

1. Otvorte `js/config.js`.
2. Nájdite riadok, ktorý chcete zmeniť, a prepíšte text medzi úvodzovkami.
3. Uložte súbor.
4. Spustite `bump_assets_version.py` (bod 1).

**Telefón — vždy obe hodnoty**

```js
phone:     "0908 41 40 91",     // ← toto uvidí návštevník
phoneHref: "+421908414091",     // ← toto sa vytočí po kliknutí (bez medzier)
```

**Otváracie hodiny**

```js
hours: [
  { d: "Pondelok – Piatok", h: "7:30 – 17:30" }
]
```

Riadky môžete pridávať aj uberať, poradie zostane. Napríklad:

```js
hours: [
  { d: "Pondelok – Piatok", h: "7:30 – 17:30" },
  { d: "Sobota",            h: "9:00 – 12:00" }
]
```

**Adresa prevádzky** (kam chodia rodičia):

```js
showroom: { full: "Gustáva Mallého 2, 851 01 Bratislava" }
```

Keď meníte adresu, zmeňte aj odkaz na mapu o pár riadkov nižšie:

```js
maps: { directLink: "https://www.google.com/maps/search/?api=1&query=…" }
```

### ⚠ Tri miesta, ktoré sa z `config.js` neplnia

Tieto treba prepísať **ručne**:

| Kde | Čo tam je | Súbor |
|---|---|---|
| Anglické stránky | otváracie hodiny (`Monday – Friday`) | prekladová mapa v `scripts/build_site.py` |
| Údaje pre Google | adresa, hodiny, súradnice v bloku `application/ld+json` | `index.html`, hore v `<head>` |
| Mapa stránok | zoznam adries (dátumy sa dopĺňajú samy) | `scripts/aktualizuj_sitemap.py` |

Prečo: anglické stránky by inak zobrazovali slovenské názvy dní, a blok pre
Google číta vyhľadávač ešte predtým, než sa spustí akýkoľvek JavaScript.

---

## 3. Zmena textu na stránke

Texty sú priamo v HTML súboroch. Ktorý súbor je ktorá stránka:

| Stránka | Súbor |
|---|---|
| Úvod | `index.html` |
| Ponuka | `ponuka.html` |
| Kurzy AJ pre deti | `kurzy.html` |
| Naša filozofia | `filozofia.html` |
| Na návšteve u nás | `na-navsteve.html` |
| Kontakt | `kontakt.html` |
| Chybová stránka | `404.html` |

**Postup**

1. Otvorte súbor v editore.
2. Nájdite text (v editore `Ctrl+F` / `Cmd+F`).
3. Prepíšte **len text medzi značkami**, značky nechajte tak:

```html
<p>Tento text môžete prepísať.</p>
   ↑                            ↑
   toto nechajte                 toto nechajte
```

4. Uložte a spustite:

```bash
python3 scripts/build_site.py
python3 .claude/skills/local-business-website/scripts/bump_assets_version.py
```

5. Súbor otvorte dvojklikom a pozrite sa, či je všetko v poriadku.

> **Prečo ten skript.** Hlavička, pätička aj celá anglická verzia sa
> **generujú**. Skript ich po vašej úprave prepíše, aby všetkých trinásť
> stránok zostalo rovnakých. Bez neho by sa slovenská a anglická verzia
> rozišli.

> Pri texte v `<title>` a v `<meta name="description">` pozor: práve tie sa
> zobrazujú v Google. **Nie sú v HTML súbore** — sú v `scripts/build_site.py`
> v tabuľke `META`. Titulok držte do 60 znakov, popis do 160.

### ⚠ Čo NEUPRAVOVAŤ ručne

| Čo | Kde to zmeniť namiesto toho |
|---|---|
| stránky v priečinku `en/` | prekladová mapa `TRANSLATE` v `scripts/build_site.py` |
| menu, hlavička, pätička | `scripts/build_site.py` |
| titulky a popisy pre Google | tabuľka `META` v `scripts/build_site.py` |

Tieto súbory a časti sa pri každom spustení skriptu prepíšu, takže by sa
vaša úprava stratila.

---

## 4. Výmena alebo pridanie fotky

**Postup**

1. Fotku uložte do `assets/img/`. Šírka aspoň 1600 px, formát JPG.
2. Názov súboru napíšte bez diakritiky a bez medzier, radšej opisne:
   `deti-rannykruh-herna.jpg`, nie `IMG_2841.jpg`.
3. V HTML nájdite starú fotku a prepíšte cestu a popis:

```html
<img src="assets/img/herna-interier-hracky.jpg"
     width="1600" height="1067"
     alt="Herňa BABYLAND – detský nábytok, police s hračkami a rastliny">
```

4. **`width` a `height` musia sedieť so skutočnými rozmermi fotky.** Keď
   nesedia, stránka počas načítavania poskočí. Rozmery zistíte v ktoromkoľvek
   prehliadači obrázkov.
5. **`alt` vždy vyplňte** — číta ho Google aj nevidiaci návštevníci. Popíšte,
   čo je na fotke, nie „fotka" alebo „obrázok".

> **Súhlas rodičov.** Ak sú na fotke tváre detí, potrebujete od rodičov súhlas
> so zverejnením. Štyri fotky prevzaté zo starého webu boli verejné už predtým,
> ale súhlasy si prosím overte.

**Veľký obrázok na úvodnej stránke** je zatiaľ zástupný (`assets/img/hero.svg`
— kreslené pozadie, nie fotka). Keď budete mať vlastnú fotku, nahraďte cestu
k `hero.svg` v `index.html` aj `en/index.html`.

---

## 5. Pridanie novej stránky do menu

Menu, hlavičku aj pätičku generuje `scripts/build_site.py`, takže stránku
pridávate **na jednom mieste** — nie do trinástich súborov.

**Postup**

1. **Vytvorte slovenský súbor** — skopírujte niektorú existujúcu stránku,
   napríklad `kurzy.html`, a premenujte ju. Bez diakritiky v názve: nie
   `krúžky.html`, ale `kruzky.html`.
2. **Prepíšte v ňom len obsah medzi `<main>` a `</main>`.** Hlavičku, pätičku
   ani `<head>` neupravujte — skript ich pri prvom spustení prepíše.
3. **Zapíšte stránku do `scripts/build_site.py`.** Do zoznamu `PAGES` pridajte
   riadok — sú v ňom štyri údaje: slovenský súbor, anglický súbor, položka
   v slovenskom menu a položka v anglickom menu:

```python
("kruzky.html", "clubs.html", "Krúžky", "Clubs"),
```

4. **Doplňte titulok a popis pre Google** do tabuľky `META` v tom istom
   súbore — štyri hodnoty: slovenský titulok, slovenský popis, anglický
   titulok, anglický popis:

```python
"kruzky.html": (
    "Krúžky pre deti | BABYLAND Bratislava",
    "Popis pre Google, do 160 znakov.",
    "Clubs for children | BABYLAND Bratislava",
    "The same description in English."),
```

5. **Doplňte preklady textov** do zoznamu `TRANSLATE` — pre každú slovenskú
   vetu na novej stránke jednu dvojicu. Ak na niektorú zabudnete, skript vás
   na to upozorní a skončí chybou.
6. **Spustite generátor:**

```bash
python3 scripts/build_site.py
```

   Vytvorí sa `en/clubs.html`, do menu a pätičky sa doplní nová položka na
   všetkých stránkach a aktuálna položka sa sama podčiarkne.

7. **Doplňte stránku do mapy stránok** — v `scripts/aktualizuj_sitemap.py`
   do zoznamu `PAGES` pridajte obidva súbory:

```python
("kruzky.html", "0.7"),
("en/clubs.html", "0.5"),
```

   a spustite `python3 scripts/aktualizuj_sitemap.py`.

8. **Ak stránka nahrádza inú**, pridajte do `netlify.toml` presmerovanie zo
   starej adresy — inak dostane každý, kto má na ňu odkaz, chybovú stránku.
   Vzory sú tam hore, stačí ich skopírovať.
9. Spustite kontrolu (bod 10).

> **⚠ Po siedmej položke menu premerajte hranicu hamburgeru.** Menu sa musí
> zmestiť do jedného riadka; dnes na to treba 1149 px po slovensky a 1162 px
> po anglicky. Ôsma položka to pretlačí a stránka sa začne dať posúvať do
> strany na bežných rozlíšeniach. Postup merania je popísaný v komentári
> v `css/styles.css` pri `@media (max-width: 1161px)`.

---

## 6. Pridanie položky do zoznamu alebo novej karty

**Odrážka s fajočkou** (zoznamy typu „Garantujeme"):

```html
<ul class="tick-list mt-1">
  <li>malé skupinky</li>
  <li>vaša nová položka</li>   ← pridajte takýto riadok
</ul>
```

Farba fajočky sa strieda automaticky (oranžová, zelená, žltá, modrá) — netreba
nič nastavovať.

> **Nová položka potrebuje aj preklad.** Doplňte dvojicu do zoznamu
> `TRANSLATE` v `scripts/build_site.py` (bod 8) a spustite generátor. Bez toho
> skript skončí chybou a povie vám, ktorý text ostal slovenský.

**Nová karta** (tri farebné boxy na úvode):

```html
<article class="card">
  <div class="card__icon"><svg …>…</svg></div>
  <h3>Nadpis karty</h3>
  <p>Jedna až dve vety.</p>
  <p><a href="stranka.html">Text odkazu</a></p>
</article>
```

Kartu vložte dovnútra `<div class="grid grid-3">`. Farba karty sa tiež strieda
automaticky podľa poradia. Ikonu skopírujte z inej karty alebo si stiahnite
z [Lucide](https://lucide.dev) (vložte `<svg>` kód priamo).

**Nová sekcia** s farebným podkladom:

```html
<section class="section section--sky">
  <div class="container container--narrow">
    <h2>Nadpis sekcie</h2>
    <p>Text…</p>
  </div>
</section>
```

Podklady na výber: `section--alt` (krémová), `section--sun` (žltkastá),
`section--sky` (modrastá), alebo žiadny (biela).

---

## 7. Zmena farieb

Všetky farby sú hore v `css/styles.css` v bloku `:root`:

```css
--c-accent:     #FF9933;   /* oranžová z loga — rámy, prúžky, ikony */
--c-accent-600: #A85400;   /* text a tlačidlá */
```

**Dôležité:** `--c-accent` je **dekoratívna**. Biely text na nej má kontrast
len 2,1 : 1, norma žiada 4,5 : 1. Na text a na tlačidlá s bielym popisom
používajte `--c-accent-600`.

Po zmene farieb **vždy** spustite kontrolu kontrastu:

```bash
node .claude/skills/local-business-website/scripts/audit_browser.js http://localhost:8000
```

---

## 8. Úprava anglickej verzie

**Anglické súbory neupravujte.** Sú to preklady slovenských stránok a pri
každom spustení `build_site.py` sa prepíšu.

Anglická verzia má rovnaké stránky, rovnaké menu aj rovnaké rozloženie ako
slovenská — líši sa len jazykom. Vzniká tak, že skript vezme obsah slovenskej
stránky a prepíše v ňom texty podľa prekladovej mapy.

**Postup pri zmene anglického textu**

1. Otvorte `scripts/build_site.py` a nájdite zoznam `TRANSLATE`.
2. Nájdite dvojicu so slovenským textom a prepíšte anglickú polovicu:

```python
("Krásny deň!", "Have a lovely day!"),
   ↑ slovenský originál   ↑ toto meníte
```

3. Spustite `python3 scripts/build_site.py`.

**Keď meníte slovenský text**, ktorý má v mape svoju dvojicu, musíte v nej
prepísať aj slovenskú polovicu — inak sa preklad prestane uplatňovať. Skript
vás na to upozorní: na konci vypíše, ktoré slová v anglickej verzii ostali
slovenské, a skončí chybou.

Čo skript rieši sám:

- otváracie hodiny na anglických stránkach sa nevypĺňajú z `config.js`
  (sú v ňom slovenské názvy dní) — ostávajú napísané v HTML;
- v angličtine sa **používa dlhá pomlčka „—"** a **nedávajú sa nezalomiteľné
  medzery** — je to opačne než v slovenčine;
- slovenský text v anglickej stránke (obchodné meno, položky menu) dostane
  `lang="sk"`, inak ho čítačka obrazovky prečíta s anglickou výslovnosťou.

---

## 9. Pravidlá pre slovenský text

Tieto tri veci stráži kontrolný skript (bod 10) — keď ich porušíte, upozorní vás.

**Pomlčka.** V slovenčine sa používa `–` (kratšia), nie `—` (dlhá). V editore
ju napíšete `Alt` + `0150` (Windows) alebo `Alt` + `-` (Mac).

```html
<p>malé skupinky – individuálny prístup</p>   ✅
<p>malé skupinky — individuálny prístup</p>   ❌
```

**Nezalomiteľná medzera po jednopísmenových slovách.** Aby predložka
nezostala visieť sama na konci riadka — na mobile sa to inak stáva takmer
v každom odseku. Píše sa `&nbsp;` namiesto medzery:

```html
<p>deti sa učia v&nbsp;malých skupinkách a&nbsp;s&nbsp;láskou</p>   ✅
<p>deti sa učia v malých skupinkách a s láskou</p>                  ❌
```

Týka sa písmen **a, i, o, u, v, s, z, k** (aj s veľkým začiatočným písmenom).

**Úvodzovky.** Slovenské sú `„takto"`, nie `"takto"`.

---

## 10. Kontrola pred zverejnením

Spustite tieto štyri príkazy v priečinku projektu. Prvé dva nepotrebujú nič
navyše, tretí a štvrtý potrebujú Node.js.

```bash
# 0. prestavanie stránok (po každej úprave textu alebo prekladu)
python3 scripts/build_site.py

# 1. pravidlá tohto webu (typografia, nadpisy, obrázky, mŕtve štýly,
#    zhoda hlavičiek a pätičiek, zhoda údajov s config.js)
python3 scripts/kontrola.py

# 2. odkazy, verzie súborov, štruktúra
python3 .claude/skills/local-business-website/scripts/audit_html.py

# 3. spustite lokálny server a nechajte bežať v druhom okne
python3 -m http.server 8000

# 4. kontrast, dotykové plochy, pretečenie na mobile
node .claude/skills/local-business-website/scripts/audit_browser.js http://localhost:8000

# 5. chyby JavaScriptu, chýbajúce súbory + snímky obrazovky
node .claude/skills/local-business-website/scripts/verify_site.js http://localhost:8000

# 6. záťažový test rozloženia (server si spúšťa sám, netreba bod 3)
node scripts/stress_test.js
```

Šiesty skript sa web snaží **rozbiť**: prejde 11 stránok na šiestich šírkach
v troch scenároch — bežne, so zväčšenými rozostupmi textu podľa WCAG 1.4.12
a s dlhým nezalomiteľným slovom v nadpise — a nakoniec skontroluje, či sa pri
otvorenom mobilnom menu nedá tabulátorom dostať za prekryv. Každý z tých
scenárov našiel na tomto webe skutočnú chybu vtedy, keď ostatné kontroly
hlásili zelenú.

Všetko musí skončiť zeleným `✅`. Upozornenie „chýba cookie lišta" je
v poriadku — web zámerne nepoužíva cookies ani meranie návštevnosti.

---

## 11. Keď sa niečo pokazí

**Stránka je celá biela alebo rozhádzaná** → v HTML je nezavretá značka.
Otvorte súbor a hľadajte, kde chýba `</p>`, `</div>` alebo `>`. Editor
VS Code takéto miesto zvýrazní.

**Zmena sa neprejavila** → nespustili ste príkazy z bodu 1, alebo si
prehliadač drží starú verziu. Vyskúšajte `Ctrl+Shift+R` (`Cmd+Shift+R`
na Macu).

**Zmena sa stratila** → upravili ste niečo, čo sa generuje: súbor v `en/`,
hlavičku, pätičku alebo titulok. Generátor to pri spustení prepísal. Zoznam
takých miest je na konci bodu 3.

**Generátor skončí chybou „NEPRELOŽENÉ ZVYŠKY"** → zmenili ste slovenskú vetu,
ktorá má v mape `TRANSLATE` svoju dvojicu, ale nezmenili ste tam slovenskú
polovicu. Skript vypíše, ktoré slová ostali slovenské — nájdite ich v mape
a opravte (bod 8).

**Kontrola hlási „hlavička sa medzi stránkami líši"** → niekto upravil
vygenerovaný súbor ručne. Spustite `python3 scripts/build_site.py` a rozdiel
zmizne.

**Telefón sa zobrazuje starý** → zmenili ste len `phone`, nie `phoneHref`
(bod 2).

**Fotka sa nezobrazuje** → skontrolujte, či názov súboru v `src=""` sedí
**presne**, vrátane veľkých a malých písmen. `Herna.jpg` a `herna.jpg` sú
pre server dva rôzne súbory.

**Menu sa na počítači nezobrazuje, je tam hamburger** → pridali ste položku
a menu sa už do riadka nezmestí. Pozrite poznámku v bode 5.

**Chcete sa vrátiť k predošlej verzii** → celý web je v Git repozitári.
Napíšte `git log`, nájdite verziu a `git checkout <číslo> -- .`
