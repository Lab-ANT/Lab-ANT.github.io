(function () {
  "use strict";

  function normalize(text) {
    return (text || "").replace(/\s+/g, " ").trim().toLowerCase();
  }

  document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("publication-search");
    const clearButton = document.getElementById("publication-search-clear");
    const count = document.getElementById("publication-search-count");
    const noResults = document.getElementById("publication-no-results");

    const items = Array.from(document.querySelectorAll(".publication-item"));
    const groups = Array.from(document.querySelectorAll(".publication-year-group"));

    if (!input || !count) return;

    const total = items.length;

    function applyFilter() {
      const query = normalize(input.value);
      const tokens = query ? query.split(/\s+/).filter(Boolean) : [];
      let visible = 0;

      items.forEach(function (item) {
        const haystack = normalize(item.getAttribute("data-search"));
        const match = tokens.every(function (token) {
          return haystack.includes(token);
        });

        item.hidden = !match;
        if (match) visible += 1;
      });

      groups.forEach(function (group) {
        const hasVisible = Array.from(
          group.querySelectorAll(".publication-item")
        ).some(function (item) {
          return !item.hidden;
        });

        group.hidden = !hasVisible;
      });

      count.textContent = query
        ? visible + " of " + total + " publications"
        : total + " publications";

      if (clearButton) clearButton.hidden = !query;
      if (noResults) noResults.hidden = visible !== 0;
    }

    input.addEventListener("input", applyFilter);

    if (clearButton) {
      clearButton.addEventListener("click", function () {
        input.value = "";
        input.focus();
        applyFilter();
      });
    }

    input.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        input.value = "";
        applyFilter();
      }
    });

    applyFilter();
  });
})();
