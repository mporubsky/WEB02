/* =========================================================================
   BABYLAND — spoločná logika webu
   -------------------------------------------------------------------------
   Robí presne štyri veci:
     1. doplní údaje z js/config.js do stránky (atribúty data-mh…)
     2. vykreslí otváracie hodiny
     3. doplní aktuálny rok do pätičky
     4. obsluhuje mobilné menu a tieň hlavičky pri skrolovaní

   Web nepoužíva formuláre, cookies ani meranie návštevnosti, takže tu nie je
   ani žiadny kód, ktorý by čokoľvek odosielal alebo sledoval.
   ========================================================================= */
(function () {
  "use strict";

  var CFG = window.MH_CONFIG || {};
  var B = CFG.business || {};

  /* Bezpečné čítanie vnorenej hodnoty, napr. get("business.showroom.full") */
  function get(path) {
    return path.split(".").reduce(function (o, k) {
      return (o && o[k] !== undefined && o[k] !== null) ? o[k] : undefined;
    }, CFG);
  }

  /* 1) Doplnenie údajov z config.js -------------------------------------
     data-mh="cesta"       → nahradí text prvku
     data-mh-tel           → nastaví odkaz tel:
     data-mh-mail          → nastaví odkaz mailto:
     data-mh-href="cesta"  → nastaví odkaz z config.js                    */
  function bindData() {
    document.querySelectorAll("[data-mh]").forEach(function (el) {
      var val = get(el.getAttribute("data-mh"));
      // Prázdna hodnota v config.js = v HTML ostane pôvodný text.
      if (val !== undefined && val !== "") el.textContent = val;
    });
    document.querySelectorAll("[data-mh-tel]").forEach(function (el) {
      if (B.phoneHref) el.setAttribute("href", "tel:" + B.phoneHref);
    });
    document.querySelectorAll("[data-mh-mail]").forEach(function (el) {
      if (B.email) el.setAttribute("href", "mailto:" + B.email);
    });
    document.querySelectorAll("[data-mh-href]").forEach(function (el) {
      var val = get(el.getAttribute("data-mh-href"));
      if (val) el.setAttribute("href", val);
    });
  }

  /* 2) Otváracie hodiny --------------------------------------------------
     Vykresľuje sa len na slovenských stránkach; anglické majú hodiny
     napísané priamo v HTML, aby v nich neboli slovenské názvy dní.        */
  function renderHours() {
    var host = document.querySelector("[data-mh-hours]");
    if (!host || !Array.isArray(B.hours)) return;
    host.innerHTML = B.hours.map(function (row) {
      return '<div class="hours-row"><span>' + row.d + "</span><b>" + row.h + "</b></div>";
    }).join("");
  }

  /* 3) Aktuálny rok v pätičke -------------------------------------------- */
  function setYear() {
    document.querySelectorAll("[data-mh-year]").forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  }

  /* 4a) Mobilné menu ----------------------------------------------------- */
  function initNav() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("main-nav");
    if (!toggle || !nav) return;

    var iconOpen = toggle.querySelector(".icon-open");
    var iconClose = toggle.querySelector(".icon-close");

    function setState(open) {
      nav.classList.toggle("is-open", open);
      document.body.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (iconOpen) iconOpen.style.display = open ? "none" : "";
      if (iconClose) iconClose.style.display = open ? "block" : "none";
    }

    toggle.addEventListener("click", function () {
      setState(!nav.classList.contains("is-open"));
    });
    // Klik na položku menu, Escape aj prechod na širokú obrazovku menu zavrú.
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { setState(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setState(false);
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 940) setState(false);
    });
  }

  /* 4b) Tieň hlavičky pri skrolovaní ------------------------------------- */
  function initHeaderScroll() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    function onScroll() { header.classList.toggle("is-scrolled", window.scrollY > 8); }
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  function init() {
    bindData();
    renderHours();
    setYear();
    initNav();
    initHeaderScroll();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
