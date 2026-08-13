/* =========================================================================
   BABYLAND — spolocna logika webu
   -------------------------------------------------------------------------
   Jediny skript na celom webe. Robi presne styri veci:

     1. doplni udaje z js/config.js do stranky (atributy data-mh…)
     2. vykresli tabulku otvaracich hodin
     3. doplni aktualny rok do paticky
     4. obsluhuje mobilne menu a tien hlavicky pri skrolovani

   Web nepouziva formulare, cookies ani meranie navstevnosti, takze tu nie je
   ziadny kod, ktory by cokolvek odosielal alebo sledoval. Ked stranka nema
   prvok, ktory dana funkcia obsluhuje, funkcia sa ticho ukonci — kazdu z nich
   je preto bezpecne spustit na ktorejkolvek stranke.

   Nazvy v tomto subore su zamerne bez diakritiky, aby sa neriesilo kodovanie.
   Texty pre navstevnika su v HTML a v js/config.js, nie tu.
   ========================================================================= */
(function () {
  "use strict";

  /** @type {Object} Cely obsah js/config.js. Prazdny objekt, ak sa nenacital. */
  var CONFIG = window.MH_CONFIG || {};

  /** @type {Object} Skratka na CONFIG.business — pouziva sa najcastejsie. */
  var business = CONFIG.business || {};

  /**
   * Bezpecne precita vnorenu hodnotu z config.js podla bodkovej cesty.
   * Ked ktorykolvek clanok cesty chyba, vrati undefined namiesto vynimky —
   * vdaka tomu neuplny config.js nerozbije celu stranku.
   *
   * @param   {string} path  Bodkova cesta, napr. "business.showroom.full".
   * @returns {*}            Najdena hodnota, alebo undefined.
   *
   * @example
   *   readConfig("business.phone");         // "0908 41 40 91"
   *   readConfig("business.neexistuje");    // undefined
   */
  function readConfig(path) {
    return path.split(".").reduce(function (node, key) {
      return (node && node[key] !== undefined && node[key] !== null) ? node[key] : undefined;
    }, CONFIG);
  }

  /**
   * Doplni udaje z config.js na miesta oznacene atributmi data-mh… Vsetky
   * hodnoty sa vkladaju cez textContent alebo setAttribute, nikdy cez
   * innerHTML, takze sa z config.js neda vlozit HTML.
   *
   * Podporovane atributy:
   *   data-mh="cesta"       nahradi text prvku hodnotou z config.js
   *   data-mh-tel           nastavi odkazu href="tel:…" z business.phoneHref
   *   data-mh-mail          nastavi odkazu href="mailto:…" z business.email
   *   data-mh-href="cesta"  nastavi odkazu href hodnotou z config.js
   *
   * Prazdna hodnota v config.js znamena „nechaj text, ktory je v HTML" — HTML
   * tak sluzi ako zaloha, ked sa js/config.js nenacita alebo je JS vypnuty.
   *
   * @returns {void}
   *
   * @example
   *   <span data-mh="business.phone">0908 41 40 91</span>
   *   <a data-mh-tel href="tel:+421908414091">Zavolajte nam</a>
   */
  function applyConfigToPage() {
    document.querySelectorAll("[data-mh]").forEach(function (el) {
      var value = readConfig(el.getAttribute("data-mh"));
      if (value !== undefined && value !== "") el.textContent = value;
    });

    document.querySelectorAll("[data-mh-tel]").forEach(function (el) {
      if (business.phoneHref) el.setAttribute("href", "tel:" + business.phoneHref);
    });

    document.querySelectorAll("[data-mh-mail]").forEach(function (el) {
      if (business.email) el.setAttribute("href", "mailto:" + business.email);
    });

    document.querySelectorAll("[data-mh-href]").forEach(function (el) {
      var value = readConfig(el.getAttribute("data-mh-href"));
      if (value) el.setAttribute("href", value);
    });
  }

  /**
   * Vykresli tabulku otvaracich hodin do prvku s atributom data-mh-hours
   * podla pola business.hours. Riadky sa skladaju z DOM prvkov, nie zo
   * spajaneho HTML, takze znaky ako & alebo < v config.js nic nerozbiju.
   *
   * Bezi len na slovenskych strankach — anglicke maju hodiny napisane priamo
   * v HTML, aby v nich neboli slovenske nazvy dni, a atribut data-mh-hours
   * teda nemaju.
   *
   * @returns {void}
   *
   * @example
   *   // config.js: hours: [{ d: "Pondelok – Piatok", h: "7:30 – 17:30" }]
   *   // HTML:      <div class="hours" data-mh-hours></div>
   *   // vysledok:  <div class="hours-row"><span>Pondelok – Piatok</span><b>7:30 – 17:30</b></div>
   */
  function renderOpeningHours() {
    var host = document.querySelector("[data-mh-hours]");
    if (!host || !Array.isArray(business.hours)) return;

    var rows = document.createDocumentFragment();
    business.hours.forEach(function (item) {
      var row = document.createElement("div");
      row.className = "hours-row";

      var day = document.createElement("span");
      day.textContent = item.d;

      var time = document.createElement("b");
      time.textContent = item.h;

      row.appendChild(day);
      row.appendChild(time);
      rows.appendChild(row);
    });

    host.textContent = "";
    host.appendChild(rows);
  }

  /**
   * Doplni aktualny rok do vsetkych prvkov s atributom data-mh-year.
   * Pouziva sa v copyrighte v paticke, aby sa rok nemusel prepisovat rucne.
   *
   * @returns {void}
   *
   * @example
   *   <span data-mh-year>2026</span>   →   <span data-mh-year>2027</span>
   */
  function fillCurrentYear() {
    document.querySelectorAll("[data-mh-year]").forEach(function (el) {
      el.textContent = String(new Date().getFullYear());
    });
  }

  /**
   * Obsluhuje mobilne menu: otvaranie a zatvaranie hamburgerom, prepinanie
   * ikony, stav aria-expanded pre citacky obrazovky a zamknutie skrolovania
   * stranky pod otvorenym menu.
   *
   * Menu sa zavrie po kliknuti na polozku, po stlaceni Escape a po rozsireni
   * okna na desktop. Hranica desktopu sa NECITA z konstanty — zistuje sa tak,
   * ze sa pozrie, ci je hamburger este zobrazeny. Vdaka tomu staci zmenit
   * media query v css/styles.css a JS sa prisposobi sam; ked tu bola pevna
   * hodnota, po posune hranice v CSS sa menu v pasme medzi starou a novou
   * hodnotou pri zmene velkosti okna samo zatvaralo.
   *
   * Kym je menu otvorene, zvysok stranky sa oznaci ako inert — inak by sa
   * tabulatorom dalo prejst za menu na odkazy, ktore su prekryte a nevidno
   * ich, a citacky obrazovky by ich cistali tiez. Zameranie sa pri otvoreni
   * presunie na prvu polozku menu a pri zatvoreni spat na hamburger.
   *
   * @returns {void}
   *
   * @example
   *   <button class="nav-toggle" aria-controls="main-nav" aria-expanded="false">
   *     <svg class="icon-open">…</svg><svg class="icon-close">…</svg>
   *   </button>
   *   <nav id="main-nav">…</nav>
   */
  function initMobileNav() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("main-nav");
    if (!toggle || !nav) return;

    var header = toggle.closest(".site-header");
    var iconOpen = toggle.querySelector(".icon-open");
    var iconClose = toggle.querySelector(".icon-close");

    /* Vsetko okrem hlavicky — hlavicka musi zostat pristupna, su v nej
       telefon aj samotny hamburger. */
    var background = Array.prototype.filter.call(document.body.children, function (el) {
      return el !== header && el.tagName !== "SCRIPT";
    });

    /**
     * Prepne menu do zadaneho stavu vratane pristupnosti pozadia.
     * @param {boolean} open  true = otvorit, false = zavriet.
     * @returns {void}
     */
    function setOpen(open) {
      nav.classList.toggle("is-open", open);
      document.body.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (iconOpen) iconOpen.style.display = open ? "none" : "";
      if (iconClose) iconClose.style.display = open ? "block" : "none";

      /* Starsie prehliadace inert nepoznaju; tam sa nic nestane a menu
         funguje ako predtym — len bez tejto ochrany. */
      if ("inert" in HTMLElement.prototype) {
        background.forEach(function (el) { el.inert = open; });
      }
    }

    /**
     * Je hamburger prave zobrazeny? Ked nie, sme na desktope a menu je
     * bezny vodorovny pruh, ktory sa nema co otvarat ani zatvarat.
     * @returns {boolean}
     */
    function isCollapsed() {
      return window.getComputedStyle(toggle).display !== "none";
    }

    toggle.addEventListener("click", function () {
      var open = !nav.classList.contains("is-open");
      setOpen(open);
      /* Menu je v HTML pred hamburgerom, takze tabulator by z hamburgeru
         viedol mimo neho. Preto sa zameranie presunie dovnutra rucne. */
      if (open) {
        var first = nav.querySelector("a");
        if (first) first.focus();
      } else {
        toggle.focus();
      }
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () { setOpen(false); });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key !== "Escape" || !nav.classList.contains("is-open")) return;
      setOpen(false);
      toggle.focus();
    });

    window.addEventListener("resize", function () {
      if (!isCollapsed()) setOpen(false);
    });
  }

  /**
   * Prida hlavicke triedu is-scrolled, len co je stranka zrolovana nizsie ako
   * 8 px. CSS na to naviaza tien, aby sa hlavicka oddelila od obsahu pod nou.
   *
   * @returns {void}
   *
   * @example
   *   .site-header.is-scrolled { box-shadow: var(--shadow); }
   */
  function initHeaderShadow() {
    var header = document.querySelector(".site-header");
    if (!header) return;

    function updateShadow() {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    }

    updateShadow();
    window.addEventListener("scroll", updateShadow, { passive: true });
  }

  /**
   * Spusti vsetky casti v poradi: najprv sa doplnia udaje, potom sa navesia
   * obsluhy udalosti.
   * @returns {void}
   */
  function init() {
    applyConfigToPage();
    renderOpeningHours();
    fillCurrentYear();
    initMobileNav();
    initHeaderShadow();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
