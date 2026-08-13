/* =========================================================================
   {{BUSINESS_NAME}} — Interaktívny dopytový sprievodca (3-krokový wizard)
   Krok 1: typ objektu → Krok 2: typ tienenia → Krok 3: mesto + telefón
   Po odoslaní zavolá zdieľané MH.sendLead(...) z main.js.
   ========================================================================= */
(function () {
  "use strict";
  var root = document.getElementById("wizard");
  if (!root) return;

  var state = { object: "", shading: "", city: "", phone: "" };
  var current = 0;
  var panels = Array.prototype.slice.call(root.querySelectorAll(".wizard__panel"));
  var stepItems = Array.prototype.slice.call(root.querySelectorAll(".wizard__steps li"));
  var backBtn = root.querySelector("[data-wiz-back]");
  var totalSteps = 3;

  function showStep(i) {
    current = i;
    panels.forEach(function (p, idx) { p.classList.toggle("is-active", idx === i); });
    stepItems.forEach(function (s, idx) {
      s.classList.toggle("is-active", idx === i);
      s.classList.toggle("is-done", idx < i);
    });
    if (backBtn) backBtn.hidden = (i === 0);
    var firstFocusable = panels[i].querySelector("button, input, select, textarea");
    if (firstFocusable && i > 0) { try { firstFocusable.focus({ preventScroll: true }); } catch (e) {} }
  }

  /* Výber možnosti (kroky 1 a 2) */
  root.querySelectorAll(".opt[data-value]").forEach(function (opt) {
    opt.addEventListener("click", function () {
      var group = opt.getAttribute("data-group");
      var siblings = root.querySelectorAll('.opt[data-group="' + group + '"]');
      siblings.forEach(function (s) { s.classList.remove("is-selected"); });
      opt.classList.add("is-selected");
      state[group] = opt.getAttribute("data-value");
      // automatický posun na ďalší krok
      setTimeout(function () { if (current < totalSteps - 1) showStep(current + 1); }, 220);
    });
  });

  if (backBtn) backBtn.addEventListener("click", function () { if (current > 0) showStep(current - 1); });

  /* Odoslanie posledného kroku */
  var form = root.querySelector("form");
  var msg = root.querySelector("[data-wiz-msg]");
  var successPanel = root.querySelector(".wizard__success");
  var submitBtn = form ? form.querySelector('button[type="submit"]') : null;

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      state.city = (form.querySelector('[name="city"]') || {}).value || "";
      state.phone = (form.querySelector('[name="phone"]') || {}).value || "";

      if (!state.object || !state.shading) {
        showMsg("Prosím, dokončite kroky 1 a 2.", true);
        return;
      }
      if (!state.city.trim() || !state.phone.trim()) {
        showMsg("Zadajte prosím obec/mesto aj telefónne číslo.", true);
        return;
      }
      showMsg("", false);
      if (submitBtn) { submitBtn.disabled = true; submitBtn.dataset.label = submitBtn.textContent; submitBtn.textContent = "Odosielam…"; }

      window.MH.sendLead({
        typ_dopytu: "Dopytový sprievodca (rýchly dopyt)",
        objekt: state.object,
        tienenie: state.shading,
        mesto: state.city,
        telefon: state.phone
      }, { subject: "Rýchly dopyt (wizard) – " + (window.MH.config.business.shortName || "") })
        .then(function () {
          if (successPanel) {
            panels.forEach(function (p) { p.classList.remove("is-active"); });
            stepItems.forEach(function (s) { s.classList.add("is-done"); s.classList.remove("is-active"); });
            successPanel.classList.add("is-active");
            if (backBtn) backBtn.hidden = true;
          }
        })
        .catch(function () {
          showMsg("Odoslanie zlyhalo. Zavolajte nám prosím alebo skúste znova.", true);
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = submitBtn.dataset.label || "Odoslať"; }
        });
    });
  }

  function showMsg(text, isError) {
    if (!msg) return;
    msg.textContent = text;
    msg.style.display = text ? "block" : "none";
    msg.style.color = isError ? "#d64545" : "inherit";
  }

  showStep(0);
})();
