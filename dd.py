"""Industries dropdown shared by the home and the landing pages (HTML, CSS, JS)."""
import os, re

def ic(name):
    # Tabler Icons (MIT, github.com/tabler/tabler-icons), outline set, inlined so they inherit currentColor
    svg = open(os.path.join('icons', name + '.svg'), encoding='utf-8').read()
    svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S)
    svg = re.sub(r'\s+', ' ', svg).replace(' width="24" height="24"', '').strip()
    return svg.replace('<svg ', '<svg class="ic" aria-hidden="true" ', 1)

ITEMS = [
    ('dental', 'dental.html', 'Dental practices', 'In-house plans for patients without insurance', 'dental'),
    ('veterinary', 'veterinary.html', 'Veterinary and pet care', 'Wellness plans, one account per household', 'paw'),
    ('gym-wellness', 'gym-wellness.html', 'Gyms and wellness', 'Clear tiers and recurring dues', 'barbell'),
    ('any-membership', 'any-membership.html', 'Any membership business', 'Clubs, med spas and local businesses', 'building-store'),
]

def dd_html(current=None, home='index.html'):
    rows = ''
    for slug, href, name, sub, icon in ITEMS:
        cur = ' aria-current="page"' if slug == current else ''
        rows += f'<a role="menuitem" href="{href}"{cur}><span class="dd-i">{ic(icon)}</span><span><b>{name}</b><small>{sub}</small></span></a>'
    cur = ' aria-current="page"' if current == 'mental-health' else ''
    rows += f'<a role="menuitem" href="mental-health.html"{cur}><span class="dd-i">{ic("mood-smile")}</span><span><b>Mental health <em class="dd-soon">Coming soon</em></b><small>Join the waitlist</small></span></a>'
    rows += f'<a class="dd-all" role="menuitem" href="{home}#guides">See all industries <span aria-hidden="true">&rarr;</span></a>'
    return ('<div class="dd"><button class="dd-btn" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="dd-menu">Industries '
            '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></button>'
            f'<div class="dd-menu" id="dd-menu" role="menu" aria-label="Industries">{rows}</div></div>')

DD_CSS = """
.dd { position: relative; }
.dd-btn { display: inline-flex; align-items: center; gap: 6px; border: 0; background: transparent; font: inherit; font-size: 16px; color: var(--muted); cursor: pointer; padding-block: 10px; transition: color .2s; }
.dd-btn:hover, .dd.open .dd-btn { color: var(--indigo); }
.dd-btn svg { transition: transform .2s; } .dd.open .dd-btn svg { transform: rotate(180deg); }
.dd-menu { position: absolute; top: calc(100% + 14px); left: 50%; width: 360px; transform: translate(-50%, 8px); opacity: 0; visibility: hidden; background: #fff; border: 1px solid var(--line); border-radius: 22px; padding: 8px; box-shadow: 0 40px 80px -30px rgba(0,24,74,.45); transition: opacity .18s, transform .18s, visibility .18s; z-index: 70; }
.dd.open .dd-menu { opacity: 1; visibility: visible; transform: translate(-50%, 0); }
.topbar .navlinks .dd-menu a, .dd-nope { display: flex; gap: 14px; align-items: center; padding: 12px 14px; border-radius: 14px; color: var(--ink); text-decoration: none; }
.topbar .navlinks .dd-menu a:hover, .topbar .navlinks .dd-menu a:focus-visible { background: var(--mint-soft); color: var(--ink); }
.topbar .navlinks .dd-menu a[aria-current] { background: var(--mint-soft); }
.dd-i { width: 42px; height: 42px; flex: none; border-radius: 12px; background: var(--indigo); color: var(--lime); display: grid; place-items: center; }
.dd-i svg { width: 22px; height: 22px; }
.dd-menu b { display: block; font-weight: 500; font-size: 16px; color: var(--ink); } .dd-menu small { display: block; font-size: 14px; color: var(--muted); line-height: 1.3; margin-top: 2px; }
.dd-soon { font-style: normal; font-size: 11.5px; font-weight: 500; letter-spacing: .04em; text-transform: uppercase; padding: 2px 8px; margin-left: 6px; border-radius: 999px; background: #FFF1D6; color: #8a5a00; vertical-align: 2px; }
.topbar .navlinks .dd-menu a.dd-all { justify-content: center; margin-top: 4px; border-top: 1px solid var(--line); border-radius: 0 0 14px 14px; padding: 14px; font-weight: 500; color: var(--indigo); }
@media (max-width: 820px) {
  .tb-in { grid-template-columns: 1fr auto auto; gap: 10px; }
  .tb-in .brand img { width: auto; max-width: none; height: 28px; }
  .navlinks { display: flex !important; } .navlinks > a { display: none; }
  .dd { position: static; } .dd-btn { padding: 10px 6px; }
  .dd-menu { position: fixed; left: 16px; right: 16px; top: 80px; width: auto; transform: translateY(8px); max-height: calc(100vh - 100px); overflow: auto; }
  .dd.open .dd-menu { transform: none; }
}
@media (prefers-reduced-motion: reduce) { .dd-menu, .dd-btn svg { transition: none; } }
"""

DD_JS = """
  (function () {
    var dd = document.querySelector('.dd'); if (!dd) return;
    var btn = dd.querySelector('.dd-btn'), items = dd.querySelectorAll('a[role=menuitem]');
    function set(o) { dd.classList.toggle('open', o); btn.setAttribute('aria-expanded', o); }
    btn.addEventListener('click', function () { set(!dd.classList.contains('open')); });
    document.addEventListener('click', function (e) { if (!dd.contains(e.target)) set(false); });
    dd.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { set(false); btn.focus(); return; }
      var i = Array.prototype.indexOf.call(items, document.activeElement);
      if (e.key === 'ArrowDown') { e.preventDefault(); set(true); items[(i + 1) % items.length].focus(); }
      if (e.key === 'ArrowUp') { e.preventDefault(); set(true); items[(i < 0 ? items.length - 1 : i - 1 + items.length) % items.length].focus(); }
    });
  })();
"""
