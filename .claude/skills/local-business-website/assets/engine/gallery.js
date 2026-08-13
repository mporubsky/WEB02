/* =========================================================================
   {{BUSINESS_NAME}} — Filtre galérie + „Zobraziť viac" (stránka realizácií)
   Filtruje dlaždice podľa data-category a postupne dávkuje zobrazenie,
   aby sa pri veľkom počte fotiek nenačítalo všetko naraz.
   ========================================================================= */
(function () {
  "use strict";
  var filters = document.querySelector("[data-gallery-filters]");
  var gallery = document.querySelector("[data-gallery]");
  if (!filters || !gallery) return;

  var moreBtn = document.querySelector("[data-gallery-more]");
  var tiles = Array.prototype.slice.call(gallery.querySelectorAll("[data-category]"));
  var STEP = 9;           // koľko dlaždíc pribudne naraz
  var current = "all";
  var shown = STEP;

  function matches(t) { return current === "all" || t.getAttribute("data-category") === current; }

  function render() {
    var seen = 0;
    tiles.forEach(function (t) {
      if (matches(t)) {
        seen++;
        t.classList.toggle("is-hidden", seen > shown);
      } else {
        t.classList.add("is-hidden");
      }
    });
    if (moreBtn) moreBtn.hidden = seen <= shown;
  }

  filters.addEventListener("click", function (e) {
    var btn = e.target.closest(".filter-btn");
    if (!btn) return;
    filters.querySelectorAll(".filter-btn").forEach(function (b) {
      var on = b === btn;
      b.classList.toggle("is-active", on);
      b.setAttribute("aria-pressed", on ? "true" : "false");
    });
    current = btn.getAttribute("data-filter");
    shown = STEP;
    render();
  });

  if (moreBtn) moreBtn.addEventListener("click", function () {
    shown += STEP;
    render();
  });

  render();
})();
