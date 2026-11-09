/* Accessibility pass: focus, form errors and descriptive tab relationships. */
(function () {
  var main = document.getElementById('main');
  document.querySelectorAll('.skip').forEach(function (skip) {
    skip.addEventListener('click', function () {
      if (main) { main.tabIndex = -1; main.focus({ preventScroll: true }); }
    });
  });
  // The dashboard replicas are illustrations, described by .rp's image label
  // and the adjacent walkthrough copy; their sample headings aren't page headings.
  document.querySelectorAll('.rp h1,.rp h2,.rp h3,.rp h4,.rp h5,.rp h6').forEach(function (heading) {
    heading.setAttribute('role', 'presentation');
  });
  // Ambient, muted footage repeats the industries already named by the page.
  // Keep the separate, named pause control available to assistive technology.
  document.querySelectorAll('video[muted][autoplay]').forEach(function (video) {
    video.setAttribute('aria-hidden', 'true'); video.removeAttribute('aria-label');
  });
  var slides = document.getElementById('slides');
  if (slides) {
    function syncSlides() {
      slides.querySelectorAll('.slide').forEach(function (slide) {
        var active = slide.classList.contains('on');
        slide.inert = !active; slide.setAttribute('aria-hidden', String(!active));
      });
    }
    slides.setAttribute('aria-live', 'polite'); slides.setAttribute('aria-atomic', 'true');
    syncSlides();
    ['prev', 'next', 'dots'].forEach(function (id) {
      var control = document.getElementById(id);
      if (control) control.addEventListener('click', syncSlides);
    });
  }
  var panel = document.getElementById('wt-p');
  if (panel) {
    function labelPanel() {
      var selected = document.querySelector('.wt-tabs [aria-selected="true"]');
      if (selected) panel.setAttribute('aria-labelledby', selected.id);
    }
    labelPanel();
    document.querySelectorAll('.wt-tabs [role="tab"]').forEach(function (tab) {
      tab.addEventListener('click', labelPanel);
      tab.addEventListener('keydown', function (e) {
        if (e.key === 'Home' || e.key === 'End') {
          var tabs = Array.from(document.querySelectorAll('.wt-tabs [role="tab"]'));
          var target = tabs[e.key === 'Home' ? 0 : tabs.length - 1];
          e.preventDefault(); target.focus(); target.click();
        }
      });
    });
  }
  var fields = ['name', 'email'].map(function (name) {
    return { input: document.getElementById('f-' + name), error: document.getElementById('e-' + name) };
  }).filter(function (field) { return field.input && field.error; });
  function updateErrors(focus) {
    var first;
    fields.forEach(function (field) {
      var invalid = !!field.error.textContent.trim();
      field.input.setAttribute('aria-invalid', String(invalid));
      if (invalid && !first) first = field.input;
    });
    if (focus && first) first.focus();
  }
  fields.forEach(function (field) {
    field.input.setAttribute('aria-required', 'true');
    var ids = (field.input.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean);
    if (!ids.includes(field.error.id)) ids.push(field.error.id);
    field.input.setAttribute('aria-describedby', ids.join(' '));
    field.error.setAttribute('role', 'alert');
    field.error.setAttribute('aria-atomic', 'true');
    field.input.addEventListener('input', function () {
      var valid = field.input.type === 'email' ? /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(field.input.value) : !!field.input.value.trim();
      if (valid) field.error.textContent = '';
      updateErrors(false);
    });
  });
  var next = document.getElementById('f-next');
  if (next) next.addEventListener('click', function () {
    updateErrors(true);
    if (!fields.some(function (field) { return field.error.textContent.trim(); })) {
      var calendar = document.getElementById('f-cal');
      var heading = calendar && calendar.querySelector('.bk-t');
      if (heading) { heading.tabIndex = -1; heading.focus({ preventScroll: true }); }
    }
  });
  var form = document.getElementById('demo-form');
  if (form) form.addEventListener('submit', function () { updateErrors(true); });
})();
