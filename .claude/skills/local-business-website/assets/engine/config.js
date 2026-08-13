/* =========================================================================
   {{BUSINESS_NAME}} — CENTRÁLNA KONFIGURÁCIA  (jediný súbor pre bežné zmeny)
   -------------------------------------------------------------------------
   Toto je jediný súbor, ktorý treba upraviť pri bežných zmenách: telefón,
   e-mail, otváracie hodiny, doručovanie formulárov, mapa, analytika, siete.
   Hodnoty sa automaticky prepíšu do celého webu cez atribúty data-mh v HTML
   (spracúva main.js). Miesta na doplnenie sú označené „⚠ DOPLNIŤ".

   Poznámka pre autora skillu: nahraď {{PLACEHOLDERS}} reálnymi údajmi z briefu.
   Texty komentárov nechaj v jazyku klienta (tu slovenčina) — číta ich majiteľ.
   ========================================================================= */

window.MH_CONFIG = {

  business: {
    name:      "{{BUSINESS_LEGAL_NAME}}",      // napr. "Firma s. r. o."
    shortName: "{{BUSINESS_SHORT_NAME}}",
    domain:    "{{domain.sk}}",
    url:       "https://{{domain.sk}}",
    ico:       "{{ICO}}",                        // (voliteľné) IČO / reg. číslo
    dic:       "{{DIC}}",                        // (voliteľné) DIČ
    icDph:     "{{IC_DPH}}",                     // (voliteľné) IČ DPH

    email:     "info@{{domain.sk}}",

    // ⚠ DOPLNIŤ reálne telefónne číslo (zobrazené + odkaz tel:)
    phone:     "+421 9XX XXX XXX",               // ako sa zobrazí návštevníkovi
    phoneHref: "+4219XXXXXXXX",                   // tel: formát (bez medzier)

    /* SÍDLO = registrové / fakturačné údaje (obchodný register, faktúry, GDPR).
       Overuj ho v registri, nie podľa Google profilu — často sa líšia. */
    address: {
      street: "{{ULICA A ČÍSLO}}",
      zip:    "{{PSČ}}",
      city:   "{{MESTO}}",
      full:   "{{CELÁ ADRESA SÍDLA}}"
    },

    /* PREVÁDZKA / PREDAJŇA = kam reálne chodia zákazníci. Ak sa líši od sídla,
       do pätičky, na kontakt a do JSON-LD patrí TOTO (zhoduje sa s mapou).
       Ak firma prevádzku nemá, celý blok zmaž — web použije `address`. */
    showroom: {
      street: "{{ULICA A ČÍSLO}}",
      zip:    "{{PSČ}}",
      city:   "{{MESTO}}",
      full:   "{{CELÁ ADRESA PREVÁDZKY}}"
    },

    hoursShort: "Po – Pi: 08:00 – 17:00",
    hours: [
      { d: "Pondelok – Piatok", h: "08:00 – 17:00" },
      { d: "Sobota – Nedeľa",   h: "Zatvorené" }
    ],

    coverage: ["{{Mesto1}}", "{{Mesto2}}", "{{Mesto3}}"],  // oblasti pôsobnosti
    coverageRadiusKm: 50,
    responseTime: "24 hodín"
  },

  /* ---- Orientačný cenník (stránka s cenníkom) ---------------------------
     Doplň reálne sumy, napr. "od 149 € / m²". Ak necháš hodnotu prázdnu (""),
     v tabuľke zostane východiskový text z HTML — nastav ho na neutrálne
     „Na vyžiadanie". Web sa tak dá zverejniť aj pred určením cien a NIKDY sa
     návštevníkovi nezobrazí zástupný text typu „od XX €".
     Kľúče si pomenuj podľa riadkov cenníka daného klienta.
     ---------------------------------------------------------------------- */
  pricing: {
    // Kľúče premenuj podľa riadkov cenníka klienta (exterioroveZaluzie, sieteOkenne…)
    polozka1: "",
    polozka2: "",
    montaz:   "Zameranie ZDARMA"
  },

  /* ---- Doručovanie formulárov ------------------------------------------
     Bez nastavenia formulár otvorí e-mailového klienta (mailto – funguje vždy).
     Pre odosielanie priamo z webu použi BEZPLATNÝ Web3Forms:
       1. https://web3forms.com  2. zadaj e-mail  3. vlož Access Key nižšie. */
  form: {
    web3formsKey: "",                 // ⚠ (voliteľné) napr. "a1b2c3d4-...."
    customEndpoint: ""                // alebo vlastné API
  },

  /* ---- Google mapa (embed bez API kľúča) --------------------------------
     Súradnice z Google Máp (…/@LAT,LNG,…) alebo nechaj prázdne (zástupný blok). */
  maps: {
    embedSrc: "",                     // napr. "https://maps.google.com/maps?q=48.12,17.09&z=16&output=embed"
    directLink: "https://www.google.com/maps/search/?api=1&query={{ADRESA_URLENC}}"
  },

  /* ---- Analytika (spúšťa sa AŽ po súhlase s cookies) --------------------- */
  analytics: {
    ga4Id: "",                        // ⚠ (voliteľné) "G-XXXXXXXXXX"
    gtmId: ""                         // ⚠ (voliteľné) "GTM-XXXXXXX"
  },

  /* ---- Sociálne siete / profil (prázdne = nezobrazí sa) ------------------ */
  social: {
    facebook:      "",
    instagram:     "",
    googleReviews: ""                 // odkaz na Google profil (napr. …/maps?cid=…)
  },

  /* ---- Súhrnné hodnotenie (len REÁLNE čísla — nikdy nevymýšľať!) --------- */
  reviews: {
    rating: "",                       // napr. "4,9" — doplniť reálne z Google
    count:  null                      // (voliteľné) reálny počet recenzií
  }
};
