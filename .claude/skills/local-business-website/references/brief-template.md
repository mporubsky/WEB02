# Zadanie na stavbu webu — šablóna promptu

Skopíruj celý blok nižšie do Clauda, vyplň hranaté zátvorky a pošli.
Šablóna je odvodená z reálneho projektu — každá sekcia uzatvára jednu medzeru,
ktorá sa pri ňom musela riešiť dodatočne (a niečo z toho stálo prerobenie celého
webu).

**Nevyplnené polia nevymazávaj.** Napíš `NEMÁM` alebo `DOPLNÍM NESKÔR` — je to
plnohodnotná informácia. Prázdne pole si Claude môže domyslieť, `NEMÁM` nie.

**Päť polí blokuje spustenie webu**, aj keby bolo všetko ostatné hotové:
telefón · e-mail · presná adresa prevádzky · obchodné meno s IČO · doručovanie
formulára. Ak ich nemáš, web sa dá postaviť, ale nedá sa zverejniť — a je lepšie
to vedieť na začiatku než na konci.

---

```text
Použi skill local-business-website a postav kompletný web pre firmu nižšie.
(alebo: /build-web — ak máš nainštalovaný spúšťač)

═══════════════════════════════════════════════════════════════════
1. IDENTITA FIRMY — presné, overené údaje
═══════════════════════════════════════════════════════════════════
Obchodné meno (presne ako v registri, vrátane veľkých písmen): [....]
   → pozor na veľké/malé písmená, prepíše sa na web ~40×
IČO: [....]   DIČ: [....]   IČ DPH: [.... / nie sme platca DPH]

Sídlo (z obchodného registra — pre faktúry a GDPR): [ulica, PSČ, mesto]
Prevádzka / predajňa (kam reálne chodia zákazníci): [ulica, PSČ, mesto / rovnaká ako sídlo]
   → toto sú často DVE RÔZNE adresy. Do pätičky, na kontakt a do mapy patrí
     prevádzka; do fakturačných údajov a GDPR sídlo. Ak si nie si istý, napíš to.

Telefón (reálny, na ktorý sa dá zavolať): [+421 ...]
E-mail: [....]
Otváracie hodiny vrátane víkendu: [Po–Pi ...; So ...; Ne ...]
Oblasť pôsobnosti: [mestá / okresy / dojazd v km]
Doména: [....]  (ak ešte nie je kúpená, napíš plánovanú)

═══════════════════════════════════════════════════════════════════
2. ZNAČKA
═══════════════════════════════════════════════════════════════════
Logo: [prikladám súbor / nemám]
   Formát: [SVG / PNG / len fotka alebo skan]
   → ak máš len rasterové alebo nekvalitné logo, napíš to. Claude ho vie
     vektorizovať; potrebuje to vedieť dopredu, nie po zostavení webu.
Firemné farby: [presné HEX / odvoď ich z loga / nemám, navrhni]
   → ak farby a logo nesedia, RIAĎ SA LOGOM a napíš mi to. Farby prevzaté zo
     staršieho dokumentu bývajú neaktuálne a prefarbenie hotového webu je drahé.
Tón komunikácie: [vecný a odborný / priateľský / prémiový]
Vizuálna inšpirácia: [odkazy na weby, ktoré sa mi páčia + čo presne na nich]

═══════════════════════════════════════════════════════════════════
3. CIEĽ WEBU
═══════════════════════════════════════════════════════════════════
Hlavný cieľ: [dopyty a obhliadky / telefonáty / predaj / vizitka]
Čo má návštevník urobiť: [vyplniť formulár / zavolať / prísť do predajne]
Cieľová skupina: [....]
Čím sme lepší ako konkurencia: [2–4 konkrétne veci, nie frázy]

═══════════════════════════════════════════════════════════════════
4. ŠTRUKTÚRA A TEXTY
═══════════════════════════════════════════════════════════════════
Podstránky: [Domov, Produkty, Cenník, O nás, Realizácie, Kontakt, GDPR]
Texty: [prikladám hotové / napíš ich podľa podkladov nižšie]
   → ak texty dodávam ja, použi ich DOSLOVA, neprepisuj ich.
Špeciálne prvky: [porovnávacia tabuľka / vzorkovník farieb / cenník /
                  dopytový sprievodca / galéria s filtrami / mapa / FAQ]

═══════════════════════════════════════════════════════════════════
5. PRODUKTY A SLUŽBY
═══════════════════════════════════════════════════════════════════
[Zoznam kategórií. Pri každej: čo to je, pre koho, technické parametre,
 varianty, čím sa líšia. Toto je jadro obsahu — čím konkrétnejšie, tým lepší web.]

═══════════════════════════════════════════════════════════════════
6. CENNÍK
═══════════════════════════════════════════════════════════════════
[ ] Mám reálne ceny — sú tu: [položka → cena]
[ ] Ceny zatiaľ nemám

→ Ak ceny nemám: NEDÁVAJ na web zástupné sumy typu „od XX €". Priprav tabuľku
  s neutrálnym „Na vyžiadanie" a ceny naviaž na config, nech ich viem doplniť
  na jednom mieste. Zákazník nesmie na webe vidieť nič nedokončené.

═══════════════════════════════════════════════════════════════════
7. FOTKY
═══════════════════════════════════════════════════════════════════
Mám: [počet + čoho / zatiaľ žiadne, dodám neskôr]
Pôvod: [vlastné firemné / od zákazníkov so súhlasom]
   → ak fotky ešte nemám, urob značkové zástupné obrázky a naviaž ich tak,
     aby sa reálne fotky prejavili len ich nahratím, bez zásahu do kódu.
   → fotky nikdy neber z cudzích zdrojov ani z recenzií na Googli.

═══════════════════════════════════════════════════════════════════
8. DÔVERYHODNOSŤ — len overené údaje
═══════════════════════════════════════════════════════════════════
Hodnotenie na Google: [priemer + počet recenzií / nemáme profil]
Odkaz na Google profil firmy: [....]
Referencie / recenzie na zverejnenie: [prikladám / nemám]
Čísla, ktoré smieš použiť: [napr. „stovky montáží", „od roku 2019", „50 km"]

→ PRAVIDLO: nevymýšľaj recenzie, mená, počty hviezdičiek ani konkrétne čísla.
  Ak je môj údaj vágny („stovky"), nechaj ho vágny — neprerábaj ho na „500+".
  Každé číslo na webe musí byť dohľadateľné v tomto zadaní.

═══════════════════════════════════════════════════════════════════
9. TECHNICKÉ NASTAVENIA
═══════════════════════════════════════════════════════════════════
Kam majú chodiť dopyty z formulára: [e-mail + Web3Forms kľúč / vlastné API / zatiaľ neviem]
   → bez kľúča formulár len otvorí e-mailového klienta; to nie je stav na spustenie.
Google Analytics / Tag Manager ID: [.... / nemám]
Odkaz na mapu (Google profil alebo súradnice): [....]
Sociálne siete: [Facebook, Instagram / nemáme]
Kam sa web nasadí: [GitHub Pages / Netlify / FTP hosting / poraď mi]
Jazyk webu: [slovenčina]

═══════════════════════════════════════════════════════════════════
10. AKO CHCEM PRACOVAŤ ĎALEJ
═══════════════════════════════════════════════════════════════════
Web musím vedieť aktualizovať sám, bez programátora — telefón, hodiny, ceny
a fotky nech sa menia na jednom mieste. Bez buildu, bez frameworkov.
K webu chcem README v slovenčine: čo kde upraviť, ako nasadiť, čo doplniť
pred spustením.

═══════════════════════════════════════════════════════════════════
11. KEDY JE HOTOVO
═══════════════════════════════════════════════════════════════════
Web považujem za hotový, keď:
 • prejdú všetky tri audity zo skillu (audit_html.py, audit_browser.js,
   verify_site.js) — a ak niektorý nevieš spustiť, povedz mi to;
 • na webe nie je ani jeden zástupný text viditeľný pre zákazníka;
 • každé číslo a tvrdenie viem dohľadať v tomto zadaní;
 • funguje to na mobile (bez pretečenia do strán) aj na počítači;
 • na záver mi napíšeš ZOZNAM, ČO MUSÍM DODAŤ JA a čo z toho blokuje spustenie.

Ak ti v zadaní niečo chýba alebo si niečím nie si istý, radšej sa opýtaj
alebo to viditeľne označ — nedopĺňaj to odhadom.
```

---

## Prečo je šablóna takto postavená

Každá sekcia zodpovedá chybe z reálneho projektu:

| sekcia | čo v pôvodnom zadaní chýbalo | čo to spôsobilo |
|---|---|---|
| 1 — identita | telefón bol zástupný `+421 9XX XXX XXX` | web sa nedal spustiť ani po dokončení |
| 1 — dve adresy | zadanie nerozlišovalo sídlo a predajňu | pätička, kontakt aj mapa ukazovali zlú adresu |
| 1 — DIČ/IČ DPH | úplne chýbali | dopĺňali sa dodatočne do 3 stránok |
| 1 — názov | „M&H žalúzie" vs. „M&H Žalúzie" | oprava na ~40 miestach naprieč webom |
| 2 — logo a farby | farby z dokumentu nesedeli s logom | prefarbenie celého webu (samostatný commit) |
| 6 — cenník | zadanie priamo žiadalo „od XX €" | zákazníci videli na cenníku `XX` |
| 8 — tvrdenia | „stovky montáží" bez upresnenia | vzniklo z toho nepodložené „500+" |
| 9 — formulár | doručovanie nebolo určené | dopyty končia v e-mailovom klientovi |
| 11 — definícia hotového | neexistovala | „hotový" web mal 11 chýb odhalených až auditom |

## Ako šablónu používať

1. **Vyplň, čo vieš** — zvyšok označ `NEMÁM`.
2. **Prilož podklady** v tej istej správe: logo, fotky, cenník, texty.
3. **Pošli naraz.** Zadanie po častiach vedie k prerábkam — najdrahšia zmena je
   tá, ktorá príde po zostavení webu (farby, adresa, štruktúra).
4. Keď neskôr dodáš fotky alebo ceny, staví to na hotovom webe — práve preto je
   všetko naviazané na `config.js`.
