/* =========================================================================
   {{BUSINESS_NAME}} — Spoločná logika webu (main.js)
   - Prepis firemných údajov z config.js do stránky (data-mh atribúty)
   - Mobilná navigácia
   - Tieň hlavičky pri skrolovaní
   - Cookie lišta + načítanie Google Analytics/GTM po súhlase
   - Odhaľovanie prvkov pri skrolovaní (reveal)
   - Vyplnenie roku v pätičke, mapa, sociálne siete, otváracie hodiny
   ========================================================================= */
(function () {
  "use strict";
  var CFG = window.MH_CONFIG || {};
  var B = CFG.business || {};

  /* ---------- Pomocná: bezpečný prístup do vnoreného objektu ------------ */
  function get(path) {
    return path.split(".").reduce(function (o, k) {
      return (o && o[k] !== undefined && o[k] !== null) ? o[k] : undefined;
    }, CFG);
  }

  /* ---------- 1) Prepis údajov (data-mh, data-mh-href, data-mh-tel) ----- */
  function bindData() {
    document.querySelectorAll("[data-mh]").forEach(function (el) {
      var val = get(el.getAttribute("data-mh"));
      // Prázdna hodnota v config.js = ponechá sa východiskový text v HTML
      // (napr. „Na vyžiadanie" v cenníku, kým nie sú doplnené reálne ceny).
      if (val !== undefined && val !== "") el.textContent = val;
    });
    // Odkazy typu tel: / mailto: / href
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

  /* ---------- 2) Otváracie hodiny (zoznam) ------------------------------ */
  function renderHours() {
    var host = document.querySelector("[data-mh-hours]");
    if (!host || !Array.isArray(B.hours)) return;
    host.innerHTML = B.hours.map(function (row) {
      return '<div class="hours-row"><span>' + row.d + '</span><b>' + row.h + '</b></div>';
    }).join("");
  }

  /* ---------- 3) Oblasti pôsobnosti (tagy) ------------------------------ */
  function renderCoverage() {
    var host = document.querySelector("[data-mh-coverage]");
    if (!host || !Array.isArray(B.coverage)) return;
    host.innerHTML = B.coverage.map(function (c) {
      return '<span class="pill">' + c + "</span>";
    }).join("");
  }

  /* ---------- 4) Google mapa alebo zástupný blok ------------------------ */
  function renderMap() {
    var host = document.querySelector("[data-mh-map]");
    if (!host) return;
    var M = CFG.maps || {};
    if (M.embedSrc) {
      host.classList.add("map-embed");
      host.innerHTML = '<iframe src="' + M.embedSrc + '" loading="lazy" ' +
        'referrerpolicy="no-referrer-when-downgrade" title="Mapa – ' +
        (B.shortName || "") + '" allowfullscreen></iframe>';
    } else {
      host.classList.add("map-placeholder");
      host.innerHTML =
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0Z"/><circle cx="12" cy="10" r="3"/></svg>' +
        "<p><strong>" + ((B.showroom || B.address || {}).full || "") + "</strong></p>" +
        '<a class="btn btn--secondary btn--sm" target="_blank" rel="noopener" href="' +
        (M.directLink || "#") + '">Otvoriť v Google Mapách</a>';
    }
  }

  /* ---------- 5) Sociálne siete ----------------------------------------- */
  function renderSocial() {
    var host = document.querySelector("[data-mh-social]");
    if (!host) return;
    var S = CFG.social || {};
    var items = [];
    if (S.facebook) items.push(link(S.facebook, "Facebook",
      '<path d="M14 9h3l.5-3H14V4.5c0-.9.3-1.5 1.6-1.5H17V.3C16.7.2 15.8 0 14.8 0 12.5 0 11 1.4 11 4v2H8v3h3v9h3V9Z"/>'));
    if (S.instagram) items.push(link(S.instagram, "Instagram",
      '<rect x="2" y="2" width="20" height="20" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.5" cy="6.5" r="1.3"/>'));
    if (S.googleReviews) items.push(link(S.googleReviews, "Google recenzie",
      '<path d="M12 2l2.9 6.3 6.9.6-5.2 4.5 1.6 6.7L12 16.9 5.8 20.6l1.6-6.7L2.2 9.4l6.9-.6L12 2Z"/>'));
    if (!items.length) { host.style.display = "none"; return; }
    host.innerHTML = items.join("");

    function link(href, label, svg) {
      return '<a href="' + href + '" target="_blank" rel="noopener" aria-label="' + label +
        '"><svg viewBox="0 0 24 24" fill="currentColor">' + svg + "</svg></a>";
    }
  }

  /* ---------- 6) Rok v pätičke ------------------------------------------ */
  function setYear() {
    document.querySelectorAll("[data-mh-year]").forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  }

  /* ---------- 7) Mobilná navigácia -------------------------------------- */
  function initNav() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("main-nav");
    if (!toggle || !nav) return;
    function close() {
      nav.classList.remove("is-open");
      document.body.classList.remove("nav-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.querySelector(".icon-open").style.display = "";
      toggle.querySelector(".icon-close").style.display = "none";
    }
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      document.body.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.querySelector(".icon-open").style.display = open ? "none" : "";
      toggle.querySelector(".icon-close").style.display = open ? "block" : "none";
    });
    nav.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", close); });
    window.addEventListener("resize", function () { if (window.innerWidth > 940) close(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  }

  /* ---------- 8) Tieň hlavičky pri skrolovaní --------------------------- */
  function initHeaderScroll() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 8); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- 9) Odhaľovanie prvkov (reveal) ---------------------------- */
  function initReveal() {
    var els = document.querySelectorAll("[data-reveal]");
    if (!els.length) return;
    if (!("IntersectionObserver" in window)) {
      els.forEach(function (el) { el.classList.add("is-visible"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-visible"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ---------- 10) Cookies + analytika ----------------------------------- */
  var CONSENT_KEY = "mh_cookie_consent";

  function loadAnalytics() {
    var A = CFG.analytics || {};
    if (A.gtmId) {
      (function (w, d, s, l, i) {
        w[l] = w[l] || []; w[l].push({ "gtm.start": new Date().getTime(), event: "gtm.js" });
        var f = d.getElementsByTagName(s)[0], j = d.createElement(s);
        j.async = true; j.src = "https://www.googletagmanager.com/gtm.js?id=" + i;
        f.parentNode.insertBefore(j, f);
      })(window, document, "script", "dataLayer", A.gtmId);
    }
    if (A.ga4Id) {
      var g = document.createElement("script");
      g.async = true; g.src = "https://www.googletagmanager.com/gtag/js?id=" + A.ga4Id;
      document.head.appendChild(g);
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag("js", new Date());
      window.gtag("config", A.ga4Id, { anonymize_ip: true });
    }
  }

  function initCookies() {
    var bar = document.getElementById("cookie-bar");
    if (!bar) return;
    var stored = null;
    try { stored = localStorage.getItem(CONSENT_KEY); } catch (e) {}

    if (stored === "accepted") { loadAnalytics(); return; }
    if (stored === "declined") { return; }

    // Zobraziť lištu (mierne oneskorene pre plynulosť)
    setTimeout(function () { bar.classList.add("is-visible"); }, 600);

    function decide(value) {
      try { localStorage.setItem(CONSENT_KEY, value); } catch (e) {}
      bar.classList.remove("is-visible");
      if (value === "accepted") loadAnalytics();
    }
    var acc = bar.querySelector("[data-cookie-accept]");
    var dec = bar.querySelector("[data-cookie-decline]");
    if (acc) acc.addEventListener("click", function () { decide("accepted"); });
    if (dec) dec.addEventListener("click", function () { decide("declined"); });
  }

  /* ---------- Inicializácia --------------------------------------------- */
  function init() {
    bindData();
    renderHours();
    renderCoverage();
    renderMap();
    renderSocial();
    setYear();
    initNav();
    initHeaderScroll();
    initReveal();
    initCookies();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else { init(); }

  /* ---------- Odoslanie dopytu (zdieľané: wizard + kontakt) --------------
     Vráti Promise. Poradie doručenia:
       1. Web3Forms (ak je nastavený form.web3formsKey)
       2. Vlastné API (ak je nastavený form.customEndpoint)
       3. mailto: fallback (otvorí e-mailového klienta) – vždy funguje
     ---------------------------------------------------------------------- */
  function sendLead(data, meta) {
    meta = meta || {};
    var F = CFG.form || {};
    var subject = meta.subject || ("Nový dopyt z webu – " + (B.shortName || ""));

    // 1) Web3Forms
    if (F.web3formsKey) {
      var payload = Object.assign({
        access_key: F.web3formsKey,
        subject: subject,
        from_name: (B.shortName || "Web") + " – formulár",
        botcheck: ""
      }, data);
      return fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(payload)
      }).then(function (r) { return r.json(); })
        .then(function (j) { if (!j.success) throw new Error(j.message || "Web3Forms error"); return j; });
    }

    // 2) Vlastné API
    if (F.customEndpoint) {
      return fetch(F.customEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.assign({ subject: subject }, data))
      }).then(function (r) { if (!r.ok) throw new Error("Endpoint error"); return r.json().catch(function () { return {}; }); });
    }

    // 3) mailto fallback
    return new Promise(function (resolve) {
      var lines = Object.keys(data).map(function (k) { return k + ": " + data[k]; });
      var href = "mailto:" + (B.email || "") +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(lines.join("\n"));
      window.location.href = href;
      resolve({ success: true, fallback: "mailto" });
    });
  }

  // Sprístupniť pomocné funkcie ďalším skriptom (wizard/form)
  window.MH = { get: get, config: CFG, sendLead: sendLead };
})();
