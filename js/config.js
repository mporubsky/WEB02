/* =========================================================================
   BABYLAND — CENTRÁLNA KONFIGURÁCIA  (jediný súbor pre bežné zmeny)
   -------------------------------------------------------------------------
   Toto je jediný súbor, ktorý treba upraviť pri bežných zmenách: telefón,
   e-mail, adresa, otváracie hodiny a odkaz na mapu.
   Hodnoty sa automaticky prepíšu do celého webu cez atribúty
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
    ]
  },

  /* ---- Odkaz na mapu ----------------------------------------------------
     Kam vedie „Zobraziť na mape" na kontaktnej stránke. */
  maps: {
    directLink: "https://www.google.com/maps/search/?api=1&query=Nobelovo+n%C3%A1m.+6%2C+Bratislava"
  }
};
