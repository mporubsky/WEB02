/* =========================================================================
   {{BUSINESS_NAME}} — Kontaktný dopytový formulár (kontaktná stránka)
   Validácia na strane prehliadača + odoslanie cez MH.sendLead(...).
   ========================================================================= */
(function () {
  "use strict";
  var form = document.getElementById("contact-form");
  if (!form) return;

  // Pozn.: hlásenie (alert) je mimo <form>, preto ho hľadáme v celom dokumente.
  var alertBox = document.querySelector("[data-form-alert]");
  var submitBtn = form.querySelector('button[type="submit"]');

  function setError(field, on) {
    var wrap = field.closest(".field") || field.closest(".check-field");
    if (wrap) wrap.classList.toggle("is-error", on);
  }

  function validate() {
    var ok = true;
    form.querySelectorAll("[required]").forEach(function (f) {
      var valid = f.type === "checkbox" ? f.checked : String(f.value).trim() !== "";
      if (valid && f.type === "email") valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.value);
      setError(f, !valid);
      if (!valid && ok) { try { f.focus(); } catch (e) {} }
      if (!valid) ok = false;
    });
    return ok;
  }

  // priebežné čistenie chýb
  form.querySelectorAll("input, select, textarea").forEach(function (f) {
    f.addEventListener("input", function () { setError(f, false); });
    f.addEventListener("change", function () { setError(f, false); });
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    showAlert("", "");
    if (!validate()) {
      showAlert("Skontrolujte prosím povinné polia označené hviezdičkou.", "fail");
      return;
    }

    var data = {
      meno:      val("name"),
      telefon:   val("phone"),
      email:     val("email"),
      mesto:     val("city"),
      produkt:   val("product"),
      popis:     val("message"),
      suhlas_gdpr: form.querySelector('[name="gdpr"]').checked ? "Áno" : "Nie"
    };

    if (submitBtn) { submitBtn.disabled = true; submitBtn.dataset.label = submitBtn.textContent; submitBtn.textContent = "Odosielam…"; }

    window.MH.sendLead(data, { subject: "Nový dopyt z kontaktného formulára – " + (window.MH.config.business.shortName || "") })
      .then(function (res) {
        form.reset();
        if (res && res.fallback === "mailto") {
          showAlert("Otvorili sme váš e-mailový program s predvyplneným dopytom. Stačí ho odoslať.", "ok");
        } else {
          showAlert("Ďakujeme! Váš dopyt sme prijali. Ozveme sa vám do " +
            (window.MH.config.business.responseTime || "24 hodín") + ".", "ok");
        }
      })
      .catch(function () {
        showAlert("Odoslanie zlyhalo. Skúste to prosím znova alebo nám zavolajte.", "fail");
      })
      .finally(function () {
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = submitBtn.dataset.label || "Odoslať nezáväzný dopyt"; }
      });
  });

  function val(name) { var el = form.querySelector('[name="' + name + '"]'); return el ? el.value.trim() : ""; }
  function showAlert(text, type) {
    if (!alertBox) return;
    alertBox.textContent = text;
    alertBox.className = "form-alert" + (type ? " is-" + type : "");
    if (text && type === "fail") { try { alertBox.scrollIntoView({ behavior: "smooth", block: "center" }); } catch (e) {} }
  }
})();
