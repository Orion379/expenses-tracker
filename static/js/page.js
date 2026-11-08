/* Behaviour for the Django-rendered pages (the data now comes from the database). */
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // Theme (stored in this browser only)
  function initTheme() {
    var theme = localStorage.getItem('et_theme') || 'ocean';
    document.body.dataset.theme = theme;
    $$('.theme-choice').forEach(function (b) { b.classList.toggle('selected', b.dataset.theme === theme); });
  }
  $$('.theme-choice').forEach(function (b) {
    b.addEventListener('click', function () {
      localStorage.setItem('et_theme', b.dataset.theme);
      initTheme();
    });
  });
  initTheme();

  // Mobile menu
  var toggle = $('#menuToggle'), sidebar = $('#sidebar');
  if (toggle && sidebar) toggle.addEventListener('click', function () { sidebar.classList.toggle('open'); });

  // Add / edit panel
  var panel = $('#entryPanel');
  if (panel) {
    var openBtn = $('#toggleForm');
    if (openBtn) openBtn.addEventListener('click', function () { panel.hidden = false; panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); });
    ['closeForm', 'cancelForm'].forEach(function (id) {
      var el = document.getElementById(id);
      if (!el) return;
      el.addEventListener('click', function () {
        // On the edit page, closing returns to the list; otherwise just hide the panel.
        if (el.dataset.listUrl) { window.location.href = el.dataset.listUrl; } else { panel.hidden = true; }
      });
    });
  }

  // Confirm before deleting
  $$('form[data-confirm]').forEach(function (f) {
    f.addEventListener('submit', function (e) { if (!window.confirm(f.dataset.confirm)) e.preventDefault(); });
  });

  // Table search (filters the rows already on the page)
  var search = $('#tableSearch'), count = $('#recordCount');
  if (search) {
    var rows = $$('#recordRows tr[data-row]');
    search.addEventListener('input', function () {
      var q = search.value.toLowerCase().trim(), visible = 0;
      rows.forEach(function (r) {
        var show = r.textContent.toLowerCase().indexOf(q) !== -1;
        r.hidden = !show;
        if (show) visible++;
      });
      var empty = $('#noMatch');
      if (empty) empty.hidden = visible !== 0 || rows.length === 0;
      if (count) count.textContent = visible + ' record' + (visible === 1 ? '' : 's');
    });
  }
})();