# Návod: ako postaviť ďalší web

Postup overený na projekte M&H Žalúzie. Cieľ: od zadania k publikovateľnému
webu bez toho, aby si opakoval chyby, ktoré sme už raz spravili.

---

## 0. Skôr než začneš — vypýtaj si od klienta päť vecí

Toto je jediná časť, ktorú nevyrieši ani skill, ani ja. **Bez týchto piatich
údajov sa web dá postaviť, ale nedá zverejniť:**

1. **Telefónne číslo**, na ktoré sa dá zavolať
2. **E-mail**
3. **Presná adresa prevádzky** (kam chodia zákazníci — býva iná než sídlo!)
4. **Obchodné meno + IČO** presne ako v registri
5. **Kam majú chodiť dopyty** z formulára

Ostatné (ceny, fotky, analytika, sociálne siete) sa dá doplniť kedykoľvek
neskôr bez zásahu do kódu.

> Ak niečo z toho klient nemá, napíš to do zadania ako `NEMÁM`. Prázdne pole
> si model domyslí, `NEMÁM` nie.

---

## 1. Založ nový repozitár

`https://github.com/new` → názov podľa klienta → **Private** → *Create*.

Ak máš od klienta podklady (logo, fotky, cenník, PDF zadanie), nahraj ich
rovno doň — Claude ich potom uvidí.

---

## 2. Dostaň skill do projektu

Pracuješ cez **claude.ai/code (web)**, takže platí: kontajner je dočasný,
**repozitár je jediné trvalé miesto.**

**Odporúčaný spôsob — samostatný repozitár so skillom (spravíš raz):**

1. Založ repozitár `claude-skills` (private)
2. Rozbaľ doň priečinok `local-business-website` zo zipu
3. Pri každom novom projekte v session napíš:

```
Pridaj repo mporubsky/claude-skills
```

Skill sa načíta automaticky aj s auditnými skriptami a šablónami.

**Alternatíva:** skopíruj priečinok `.claude/skills/local-business-website/`
do nového repozitára ručne. Funguje tiež, len to musíš robiť opakovane.

---

## 3. Zadaj úlohu

Podľa toho, čo máš po ruke:

### A) Mám hotové zadanie alebo podklady

```
/build-web

[sem vlož zadanie alebo napíš: podklady sú v priložených súboroch]
```

Alebo bez slash-príkazu:

```
Použi skill local-business-website a postav web pre firmu podľa priloženého zadania.
```

### B) Zadanie nemám, chcem ním prejsť

```
/PROMPTsablonaweb
```

Prevedie ťa šiestimi okruhmi (identita, značka, cieľ, produkty, cenník a fotky,
technika), na konci z odpovedí zostaví hotové zadanie a spýta sa, či má stavať.

### C) Klient si zadanie píše sám

Pošli mu súbor `references/brief-template.md` zo skillu. Je to vyplňovacia
šablóna s vyznačením, čo blokuje spustenie.

---

## 4. Čo sa bude diať

Skill prejde piatimi fázami. Po každej je brána — nepustí ďalej, kým niečo nesedí.

| Fáza | Čo vznikne | Na čo si dať pozor |
|---|---|---|
| **Zadanie** | zoznam údajov + čo chýba | trvaj na piatich blokujúcich poliach |
| **Základ** | skopírovaný engine, prefarbený podľa značky | **riaď sa logom, nie farbami z dokumentu** |
| **Obsah** | stránky z textov klienta | texty od klienta sa používajú doslova |
| **Materiál** | zástupné obrázky, neskôr reálne fotky | fotky skontroluj na vodoznaky fotoaparátu |
| **Kontrola** | tri audity + dva ľudské prechody | musí prejsť, alebo vedieť prečo nie |

Výsledok: statický web bez buildu — HTML + jeden CSS + niekoľko JS súborov.
Žiadny framework, žiadne závislosti, dá sa hodiť kamkoľvek.

---

## 5. Keď prídu fotky (aj neskôr)

Nahraj ich do repozitára a napíš:

```
Zoptimalizuj tieto fotky, správne ich pomenuj a poukladaj do galérie.
```

Claude ich sám roztriedi, nájde duplikáty, oreže vodoznaky a prekóduje do WebP.

**Potom si popisy prejdi očami.** Toto je jediná vec, ktorú automat neodhalí —
na M&H webe bolo **sedem fotiek popísaných zle** (interiér označený ako
exteriér, rolety ako žalúzie). Ak niečo nesedí, stačí napísať: *„fotka X je
v skutočnosti Y"*.

---

## 6. Pred zverejnením

Nechaj prebehnúť kontrolu:

```
Sprav finálny audit webu.
```

Spustí tri skripty:

| Skript | Čo kontroluje |
|---|---|
| `audit_html.py` | odkazy, kotvy, SEO, **zástupné texty viditeľné zákazníkovi** |
| `audit_browser.js` | pretečenie na mobile, kontrast, dotykové plochy |
| `verify_site.js` | chyby JavaScriptu, chýbajúce súbory, mobilné menu |

Plus dve veci, ktoré skript nezvládne:

- **Každé číslo na webe musí byť dohľadateľné v zadaní.** Ak zadanie hovorí
  „stovky", na webe je „stovky" — nie „500+".
- **Prečítaj stránky ako zákazník.** Akákoľvek veta, ktorá oslovuje majiteľa
  („doplňte ceny", „vzorová šablóna"), je chyba.

---

## 7. Publikovanie

1. Zlúč pull request do `main`
2. **Settings → Pages → Branch** prepni na `main`, ulož
3. Počkaj na nasadenie
4. **Až potom** zmaž pracovnú vetvu

> Ak vetvu zmažeš pred krokom 2, web spadne — Pages stratia zdroj.

---

## 8. Keď neskôr niečo meníš

Telefón, hodiny, ceny, adresa — všetko je na jednom mieste v `js/config.js`.

**Po každej zmene `config.js` alebo `styles.css` musí prebehnúť:**

```
python .claude/skills/local-business-website/scripts/bump_assets_version.py
```

Bez toho uvidíš staré údaje aj po oprave — prehliadač si drží starú verziu.
Presne toto raz rozbilo hero na mobile. Ak zabudneš, `audit_html.py` to
teraz nahlási ako chybu.

---

## Rýchly prehľad

**Príkazy v Claude**

| Príkaz | Kedy |
|---|---|
| `/build-web` | mám zadanie, chcem stavať |
| `/PROMPTsablonaweb` | zadanie nemám, chcem ním prejsť |
| `/postav-web` | slovenský alias pre `/build-web` |

**Skripty v skille** (`scripts/`)

| Skript | Úloha |
|---|---|
| `gen_placeholder_svgs.py` | značkové zástupné obrázky |
| `optimize_photos.py` | EXIF, zmenšenie, prekódovanie fotiek |
| `to_webp.py` | WebP + obalenie do `<picture>` |
| `render_raster.js` | náhľad pre sociálne siete + ikony |
| `bump_assets_version.py` | verzia `?v=` z obsahu súborov |
| `audit_html.py` | kontrola zdrojového kódu |
| `audit_browser.js` | kontrola vykreslenej stránky |
| `verify_site.js` | kontrola behu stránky |

**Dokumentácia v skille** (`references/`)

| Súbor | Obsah |
|---|---|
| `brief-template.md` | šablóna zadania pre klienta |
| `components.md` | 14 hotových komponentov + hlavička stránky |
| `pitfalls.md` | 25 zdokumentovaných chýb z reálnych projektov |
| `seo-legal-perf.md` | SEO, GDPR, výkon, nasadenie |

---

## Tri pravidlá, ktoré držia kvalitu

1. **Nič nevymýšľať.** Recenzie, počty realizácií, adresy, ceny — všetko musí
   pochádzať od klienta. Vágne zadanie zostáva vágne aj na webe.
2. **Nič určené majiteľovi na verejnej stránke.** Pokyny patria do `README.md`.
   Keď hodnota chýba, zákazník vidí „Na vyžiadanie", nie `XX`.
3. **Každá nájdená chyba ide späť do nástrojov.** Najprv sa zapíše do
   `pitfalls.md`, a keď sa dá zmerať, doplní sa do auditu. Tak sa nabudúce
   chytí sama.
