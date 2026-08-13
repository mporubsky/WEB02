/* =========================================================================
   BABYLAND — CENTRÁLNA KONFIGURÁCIA  (jediný súbor pre bežné zmeny)
   -------------------------------------------------------------------------
   Toto je jediný súbor, ktorý treba upraviť pri bežných zmenách: telefón,
   e-mail, otváracie hodiny, ceny, doručovanie formulárov, mapa, analytika,
   sociálne siete. Hodnoty sa automaticky prepíšu do celého webu cez atribúty
   data-mh v HTML (spracúva main.js). Miesta na doplnenie sú označené „⚠ DOPLNIŤ".

   POZOR: Ak zmeníte telefón, e-mail alebo adresu, prepíšte ich aj v bloku
   JSON-LD na konci index.html — ten sa z tohto súboru NEPLNÍ a Google by
   inak čítal starý údaj. Návod je v README.md.
   ========================================================================= */

window.MH_CONFIG = {

  business: {
    name:      "Mgr. Jana Kamenská – 1. súkromné opatrovateľské centrum BABYLAND",
    shortName: "BABYLAND",
    domain:    "babyland-centrum.sk",
    url:       "https://www.babyland-centrum.sk",
    ico:       "40 646 149",
    // Číslo živnostenského registra (namiesto DIČ – živnostník neplatca DPH)
    zivnostRegister: "106-10631",
    dic:       "",                               // ⚠ DOPLNIŤ, ak sa má uvádzať
    icDph:     "",                               // prázdne = neplatca DPH

    email:     "info@babyland-centrum.sk",

    // Telefón prevzatý z pôvodného webu – pred spustením overte, že platí.
    phone:     "0908 41 40 91",                  // ako sa zobrazí návštevníkovi
    phoneHref: "+421908414091",                  // tel: formát (bez medzier)

    /* SÍDLO = registrové / fakturačné údaje (živnostenský register, faktúry,
       GDPR – prevádzkovateľ). Nepoužíva sa v pätičke ani na mape. */
    address: {
      street: "Jána Kostku 2428/18",
      zip:    "901 01",
      city:   "Malacky",
      full:   "Jána Kostku 2428/18, 901 01 Malacky"
    },

    /* PREVÁDZKA = kam reálne chodia rodičia s deťmi. Do pätičky, na kontakt
       a do JSON-LD patrí TOTO (zhoduje sa s mapou aj Google profilom). */
    showroom: {
      street: "Nobelovo nám. 6",
      zip:    "",                                // ⚠ DOPLNIŤ PSČ prevádzky
      city:   "Bratislava",
      full:   "Nobelovo nám. 6, Bratislava"
    },

    hoursShort: "Po – Pi: 7:00 – 17:00",
    hours: [
      { d: "Pondelok – Piatok", h: "7:00 – 17:00" },
      { d: "Predĺžená opatera", h: "6:00 – 19:00 (po dohode)" },
      { d: "Sobota – Nedeľa",   h: "Po dohode" }
    ],

    coverage: ["Bratislava", "Petržalka", "Staré Mesto"],
    responseTime: ""                             // ⚠ DOPLNIŤ, ak chcete sľubovať lehotu
  },

  /* ---- Cenník ------------------------------------------------------------
     Ceny z pôvodného webu boli v slovenských korunách (rok 2004), preto sú
     tu zámerne prázdne. Kým sú prázdne, v tabuľke zostane text „Na vyžiadanie".
     Doplňte reálnu sumu v eurách, napr. "od 350 € / mesiac" – prejaví sa
     okamžite na celom webe.
     ---------------------------------------------------------------------- */
  pricing: {
    celodenna:   "",     // celodenná opatera, Po–Pi 7:00–17:00
    predlzena:   "",     // príplatok za predĺženú opateru (6:00–19:00)
    poldenna:    "",     // poldenná opatera
    hodinova:    "",     // hodinová opatera
    vecerna:     "",     // večerná / nočná opatera
    vikendova:   "",     // víkendová opatera
    celotyzdnova:"",     // celotýždňová opatera
    kurzJazyk:   "",     // kurz angličtiny / nemčiny pre deti
    obhliadka:   "Obhliadka ZDARMA"
  },

  /* ---- Doručovanie formulárov ------------------------------------------
     Bez nastavenia formulár otvorí e-mailového klienta (mailto – funguje vždy).
     Pre odosielanie priamo z webu použite BEZPLATNÝ Web3Forms:
       1. https://web3forms.com  2. zadajte e-mail  3. vložte Access Key nižšie. */
  form: {
    web3formsKey: "",                 // ⚠ DOPLNIŤ, napr. "a1b2c3d4-...."
    customEndpoint: ""
  },

  /* ---- Google mapa (embed bez API kľúča) --------------------------------
     Vyhľadáva podľa adresy prevádzky. Ak chcete presnejší bod, nahraďte
     adresu súradnicami: ...?q=48.1234,17.1050&z=16&output=embed */
  maps: {
    embedSrc:   "https://maps.google.com/maps?q=Nobelovo%20n%C3%A1m.%206%2C%20Bratislava&z=16&output=embed",
    directLink: "https://www.google.com/maps/search/?api=1&query=Nobelovo+n%C3%A1m.+6%2C+Bratislava"
  },

  /* ---- Analytika (spúšťa sa AŽ po súhlase s cookies) --------------------- */
  analytics: {
    ga4Id: "",                        // ⚠ DOPLNIŤ, ak chcete merať návštevnosť: "G-XXXXXXXXXX"
    gtmId: ""
  },

  /* ---- Sociálne siete / profil (prázdne = nezobrazí sa) ------------------ */
  social: {
    facebook:      "",                // ⚠ DOPLNIŤ odkaz na FB stránku
    instagram:     "",
    googleReviews: ""                 // odkaz na Google profil (…/maps?cid=…)
  },

  /* ---- Súhrnné hodnotenie (len REÁLNE čísla — nikdy nevymýšľať!) ---------
     Kým je rating prázdny, hodnotenie sa na webe vôbec nezobrazí. */
  reviews: {
    rating: "",                       // napr. "4,9" — doplniť reálne z Google
    count:  null
  }
};
