/* Shared progressive enhancement; no animation library or gesture simulation. */
(function () {
  var motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('.dd').forEach(function (dd) {
    var trigger = dd.querySelector('.dd-btn'), menu = dd.querySelector('.dd-menu');
    if (!trigger || !menu) return;
    function sync() { menu.inert = !dd.classList.contains('open'); }
    sync();
    trigger.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') menu.inert = false;
    }, true);
    // Existing menu handlers keep ownership of clicks and arrow keys.
    dd.addEventListener('click', sync);
    dd.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        dd.classList.remove('open'); trigger.setAttribute('aria-expanded', 'false'); trigger.focus();
      }
      if (document.querySelector('.blog-tools') && (e.key === 'ArrowDown' || e.key === 'ArrowUp')) {
        var items = Array.from(menu.querySelectorAll('a'));
        var index = items.indexOf(document.activeElement);
        e.preventDefault(); dd.classList.add('open'); trigger.setAttribute('aria-expanded', 'true'); menu.inert = false;
        items[e.key === 'ArrowDown' ? (index + 1) % items.length : (index < 0 ? items.length - 1 : (index - 1 + items.length) % items.length)].focus();
      }
      if (e.key === 'Home' || e.key === 'End') {
        var links = menu.querySelectorAll('a');
        if (dd.classList.contains('open') && links.length) {
          e.preventDefault(); links[e.key === 'Home' ? 0 : links.length - 1].focus();
        }
      }
      sync();
    });
    document.addEventListener('click', function (e) {
      if (!dd.contains(e.target)) { dd.classList.remove('open'); trigger.setAttribute('aria-expanded', 'false'); }
      sync();
    });
    dd.addEventListener('focusout', function (e) {
      if (!dd.contains(e.relatedTarget)) {
        dd.classList.remove('open'); trigger.setAttribute('aria-expanded', 'false'); sync();
      }
    });
  });
  document.querySelectorAll('video[autoplay]').forEach(function (video) {
    var parent = video.parentElement;
    if (parent.querySelector('.mc-video-control')) return;
    var button = document.createElement('button');
    button.className = 'mc-video-control'; button.type = 'button';
    function sync() {
      button.textContent = video.paused ? 'Play video' : 'Pause video';
      button.setAttribute('aria-label', button.textContent);
    }
    function stopForPreference() { if (motion.matches) { video.autoplay = false; video.pause(); } sync(); }
    button.addEventListener('click', function () {
      if (video.paused) { var play = video.play(); if (play) play.catch(sync); }
      else video.pause();
      sync();
    });
    video.addEventListener('play', sync); video.addEventListener('pause', sync);
    parent.appendChild(button); stopForPreference();
    motion.addEventListener('change', stopForPreference);
  });
})();
