/* =========================================================================
   BABYLAND — údaje centra
   -------------------------------------------------------------------------
   Toto je jediný súbor, ktorý treba upraviť pri bežných zmenách: telefón,
   e-mail, adresa, otváracie hodiny a odkaz na mapu. Hodnoty sa automaticky
   doplnia na všetky slovenské aj anglické stránky (spracúva ich js/main.js).

   PO KAŽDEJ ZMENE spustite:
     python3 .claude/skills/local-business-website/scripts/bump_assets_version.py
   inak môžu návštevníci ešte dlho vidieť staré údaje z pamäte prehliadača.

   DVE MIESTA, KTORÉ SA ODTIAĽTO NEPLNIA a treba ich prepísať ručne:
     • otváracie hodiny na anglických stránkach (en/index.html, en/contact.html)
     • blok „application/ld+json" na konci index.html — číta ho Google
   ========================================================================= */

window.MH_CONFIG = {

  business: {
    /* Obchodné meno tak, ako je v živnostenskom registri — teda meno
       ZRIAĎOVATEĽA. Prevádzka sa volá „Súkromná materská škola BABYLAND";
       „1. súkromné opatrovateľské centrum" je len časť názvu živnosti a
       patrí výhradne do fakturačných údajov na kontaktnej stránke. */
    name: "Mgr. Jana Kamenská – 1. súkromné opatrovateľské centrum BABYLAND",
    ico: "40 646 149",
    zivnostRegister: "106-10631",

    /* ⚠ Telefón a e-mail sú prevzaté z pôvodného webu (2004) —
       pred spustením overte, že stále platia. */
    phone: "0908 41 40 91",        // ako sa zobrazí návštevníkovi
    phoneHref: "+421908414091",    // na čo sa vytočí po kliknutí (bez medzier)
    email: "info@babyland-centrum.sk",

    /* SÍDLO — fakturačné údaje zo živnostenského registra.
       Zobrazuje sa len v sekcii „Fakturačné údaje" na kontakte. */
    address: {
      full: "Jána Kostku 2428/18, 901 01 Malacky"
    },

    /* PREVÁDZKA — kam reálne chodia rodičia s deťmi. Zobrazuje sa v pätičke,
       v hero karte a na kontakte, a musí sedieť s odkazom na mapu nižšie.
       Adresa je z tabuľky na prevádzke a zo zápisu na Google Maps
       („Babyland – Súkromná Materská Škola", Petržalka). */
    showroom: {
      full: "Gustáva Mallého 2, 851 01 Bratislava"
    },

    /* Krátky zápis hodín — používa sa v pätičke */
    hoursShort: "Po – Pi: 7:30 – 17:30",

    /* Tabuľka hodín — vykresľuje sa na úvode, v ponuke a na kontakte.
       Riadky môžete pridávať aj uberať, poradie sa zachová.

       Prvý riadok je prevádzková doba z tabuľky na dverách prevádzky.
       ⚠ Zvyšné dva riadky sú prevzaté z pôvodného webu (2004), keď ešte
       išlo o opatrovateľské centrum — pred spustením ich overte. */
    hours: [
      { d: "Pondelok – Piatok", h: "7:30 – 17:30" },
      { d: "Predĺžená opatera", h: "6:00 – 19:00 (po dohode)" },
      { d: "Sobota – Nedeľa",   h: "Po dohode" }
    ]
  },

  /* Kam vedie odkaz „Zobraziť na mape" na kontaktnej stránke.
     Ak by ukazoval nepresne, nahraďte adresu v odkaze súradnicami
     48.1208342, 17.0963077. */
  maps: {
    directLink: "https://www.google.com/maps/search/?api=1&query=Gust%C3%A1va+Mall%C3%A9ho+2%2C+851+01+Bratislava"
  }
};
