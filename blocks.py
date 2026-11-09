"""Shared UI blocks for the home and the landing pages: demo form with time picker, dashboard walkthrough,
sample reviews and the floating contact card. HTML is returned by functions; CSS and JS are plain strings."""
import html
from dd import ic
from replica import CSS as REPLICA_CSS

esc = html.escape

# Where demos are booked (Cal.com scheduling behind this page). While empty, the form shows a simple
# day and time request that is emailed to the team instead.
BOOK_URL = 'https://cal.com/member-cloud-lhhcvy/demo'

# ---------------------------------------------------------------- demo form
def form_html(default='dental', waitlist=False):
    opts = [('dental', 'Dental practice'), ('veterinary', 'Veterinary clinic'), ('gym', 'Gym or wellness club'), ('mental', 'Mental health practice'), ('other', 'Something else')]
    o = ''.join(f'<option value="{v}"{" selected" if v == default else ""}>{l}</option>' for v, l in opts)
    if waitlist:
        return f"""<form id="demo-form" data-mode="waitlist" novalidate>
        <div class="fstep" data-step="1">
          <div class="f"><label for="f-name">Your name</label><input id="f-name" type="text" autocomplete="name"><div class="err" id="e-name"></div></div>
          <div class="f"><label for="f-email">Work email</label><input id="f-email" type="email" autocomplete="email"><div class="err" id="e-email"></div></div>
          <div class="f"><label for="f-practice">Practice name</label><input id="f-practice" type="text" autocomplete="organization"></div>
          <div class="f"><label for="f-phone">Phone (optional)</label><input id="f-phone" type="tel" autocomplete="tel"></div>
          <input type="hidden" id="f-type-w" value="Mental health practice"><select id="f-type" hidden><option value="mental" selected>Mental health practice</option></select>
          <input type="hidden" id="f-notes" value="Waitlist: mental health practice (coming soon)">
          <input class="hp" type="text" id="f-website" tabindex="-1" autocomplete="off" aria-hidden="true">
          <button class="btn btn-dark" type="submit" id="f-send">Join the waitlist</button>
        </div>
        <div id="form-status" aria-live="polite"></div>
      </form>"""
    return f"""<form id="demo-form" novalidate data-book="{BOOK_URL}">
        <ol class="fsteps" aria-label="Progress"><li class="on" data-s="1"><b>1</b> Your details</li><li data-s="2"><b>2</b> Pick a time</li></ol>
        <div class="fstep" data-step="1">
          <div class="f"><label for="f-name">Your name</label><input id="f-name" type="text" autocomplete="name"><div class="err" id="e-name"></div></div>
          <div class="f"><label for="f-email">Work email</label><input id="f-email" type="email" autocomplete="email"><div class="err" id="e-email"></div></div>
          <div class="f"><label for="f-practice">Business name</label><input id="f-practice" type="text" autocomplete="organization"></div>
          <div class="f"><label for="f-phone">Phone (optional)</label><input id="f-phone" type="tel" autocomplete="tel"></div>
          <div class="f"><label for="f-type">Type of business</label><select id="f-type">{o}</select></div>
          <button class="btn btn-dark" type="button" id="f-next">Pick a time <span aria-hidden="true">&rsaquo;</span></button>
        </div>
        <div class="fstep" data-step="2" hidden>
          <div id="f-cal" hidden></div>
          <div id="f-picker" class="fpk">
          <div class="f"><span class="lab" id="lab-day">Pick a day</span><div class="pick days" id="f-days" role="radiogroup" aria-labelledby="lab-day"></div></div>
          <div class="f"><span class="lab" id="lab-time">Time (Eastern)</span><div class="pick times" id="f-times" role="radiogroup" aria-labelledby="lab-time"></div></div>
          <div class="f"><label for="f-notes">Anything we should know? (optional)</label><textarea id="f-notes" rows="2" maxlength="1000"></textarea></div>
          <input class="hp" type="text" id="f-website" tabindex="-1" autocomplete="off" aria-hidden="true">
          <div class="frow"><button class="btn btn-ghost" type="button" id="f-back">&lsaquo; Back</button><button class="btn btn-dark" type="submit" id="f-send">Book a free demo</button></div>
          <button class="tlink linkbtn" type="button" id="f-skip">Skip the time, just contact me</button>
          </div>
          <div class="frow" id="f-back2" hidden><button class="btn btn-ghost" type="button" id="f-back-cal">&lsaquo; Back</button></div>
        </div>
        <div id="form-status" aria-live="polite"></div>
      </form>"""

# ---------------------------------------------------------------- walkthrough
def walkthrough_html(default='dental', switch=False):
    import replica
    inds = list(replica.IND) if switch else [default]
    names = {'dental': 'Dental', 'veterinary': 'Veterinary', 'gym': 'Gym and wellness', 'any': 'Any membership'}
    c0 = replica.IND[default]
    tabs = [('dashboard', 'Dashboard'), ('patients', c0['people']), ('member', 'Member'), ('payments', 'Payments'), ('landing', c0['page_label']), ('fees', 'Fees')]
    tb = ''.join(f'<button role="tab" type="button" id="wt-t{i}" aria-controls="wt-p" aria-selected="{"true" if i == 0 else "false"}"{"" if i == 0 else " tabindex=-1"} data-k="{k}">{n}</button>' for i, (k, n) in enumerate(tabs))
    sets = ''.join(f'<div class="rp-set" data-ind="{k}" data-people="{replica.IND[k]["people"]}" data-page="{replica.IND[k]["page_label"]}"{"" if k == default else " hidden"}>{replica.panels_html(k)}</div>' for k in inds)
    sw = ''
    if switch:
        sw = '<div class="wt-inds" role="group" aria-label="Show the screens for">' + ''.join(f'<button type="button" data-ind="{k}" aria-pressed="{"true" if k == default else "false"}">{names[k]}</button>' for k in inds) + '</div>'
    return f"""<section class="lp-sec wt" id="walkthrough" data-default="{default}">
  <div class="wrap">
    <h2 class="lp-h2">A look inside the dashboard.</h2>
    <p class="lp-sub">Screens from the MemberCloud demo account, with sample data. Click through to explore.</p>
    {sw}
    <div class="wt-tabs" role="tablist" aria-label="Dashboard areas"><span class="ind" aria-hidden="true"></span>{tb}</div>
    <div class="wt-grid" id="wt-p" role="tabpanel">
      <div class="wt-copy"><h3 id="wt-h"></h3><p id="wt-d"></p><ul id="wt-l"></ul></div>
    </div>
    <div class="rp-wrap"><div class="rp-scroll"><div class="rp-box"><div class="rp" role="img" aria-label="MemberCloud dashboard screens with sample data">{sets}</div></div></div></div>
    <p class="wt-fine">Names, emails and numbers are sample data, set up the way {"each industry" if switch else "a " + names[default].lower() + " business"} would use MemberCloud.</p>
  </div>
</section>"""

# ---------------------------------------------------------------- reviews
# Real clients. The quotes are DRAFTS written for each practice to approve or edit; until they approve, the page labels
# them as drafts. Replace 'quote' with the approved wording and set draft=False.
CLIENTS = [
    dict(big='+40%', quote='In three months we grew our affiliated patients by 40%. Families understand the plan right away, and billing takes care of itself.',
         text='more affiliated patients in 3 months at Stuart Pediatric Dentistry, a dental practice running on MemberCloud.', who='Stuart Pediatric Dentistry', sub='+40% affiliated patients in 3 months', ini='SP', draft=True),
    dict(big='30+', quote='We started with no membership plan at all. In the first month we enrolled more than 30 members, and the payments run automatically.',
         text='members enrolled in the first month, starting with no membership plan. Plans are easy to present and payments run automatically.', who='Dr. Andres Cuartas, DDS', sub='Doral Dental Studio, Miami', ini='DD', draft=True),
]

def reviews_html(kind=None):
    cards = ''
    for c in CLIENTS:
        body = f'<blockquote>&ldquo;{esc(c["quote"])}&rdquo;</blockquote>' if c.get('quote') else f'<p class="rw-text">{esc(c["text"])}</p>'
        badge = '<span class="rw-draft">Draft quote, pending approval</span>' if c.get('draft') else ''
        cards += f'<figure class="rw-card">{badge}<div class="rw-big num">{esc(c["big"])}</div>{body}<figcaption><span class="rw-av" aria-hidden="true">{c["ini"]}</span><span><b>{esc(c["who"])}</b><small>{esc(c["sub"])}</small></span></figcaption></figure>'
    note = '<p class="rw-note">Draft quotes written for each practice to approve. Replace them with the approved wording before launch.</p>' if any(c.get('draft') for c in CLIENTS) else ''
    return f"""<section class="lp-sec rw" id="reviews">
  <div class="wrap">
    <h2 class="lp-h2">Practices already running on MemberCloud.</h2>
    <div class="rw-grid">{cards}</div>
    {note}
  </div>
</section>"""

# ---------------------------------------------------------------- contact card
def contact_card_html():
    return """<aside class="cc" id="cc" aria-label="Contact MemberCloud"><button class="cc-x" type="button" aria-label="Dismiss">&times;</button>
  <b>Talk to our team</b><a class="cc-tel" href="tel:+18884087007">(888) 408-7007</a>
  <a class="btn btn-dark cc-btn" href="#demo">Book a free demo</a><a class="cc-mail" href="mailto:info@member-cloud.com">info@member-cloud.com</a></aside>"""

# ---------------------------------------------------------------- CSS
CSS = REPLICA_CSS + """
/* shared section helpers (the home does not load the landing-page CSS) */
.lp-sec { padding-block: clamp(64px, 8vw, 120px); }
.lp-h2 { margin-top: 14px; color: var(--indigo); font-weight: 500; letter-spacing: -0.045em; max-width: 15em; }
.lp-sub { margin-top: 16px; color: var(--muted); max-width: 34em; font-size: 20px; }
.rv { opacity: 0; transform: translateY(18px); transition: opacity .6s ease, transform .6s ease; } .rv.in { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) { .rv { opacity: 1; transform: none; transition: none; } }
.ic { width: 1em; height: 1em; display: block; }
/* demo form steps */
.fsteps { list-style: none; display: flex; gap: 8px; margin: 0 0 18px; padding: 0; font-size: 14px; }
.fsteps li { display: flex; align-items: center; gap: 8px; padding: 7px 14px 7px 8px; border-radius: 999px; border: 1px solid var(--line); color: var(--muted); background: var(--surface); transition: all .25s; }
.fsteps li b { width: 24px; height: 24px; border-radius: 50%; background: var(--line); color: var(--ink); display: grid; place-items: center; font-size: 13px; font-weight: 600; }
.fsteps li.on { border-color: var(--indigo); color: var(--indigo); } .fsteps li.on b { background: var(--lime); color: var(--indigo-deep); }
.fpk { display: grid; gap: 14px; } .fpk[hidden] { display: none; }
.fstep[hidden] { display: none; } .fstep { display: grid; gap: 14px; animation: fIn .35s ease; }
@keyframes fIn { from { opacity: 0; transform: translateX(10px); } to { opacity: 1; transform: none; } }
.f .lab { display: block; font-size: 15px; margin-bottom: 8px; }
.pick { display: flex; flex-wrap: wrap; gap: 8px; }
.pick button { font: inherit; font-size: 15px; padding: 10px 14px; border-radius: 14px; border: 1px solid var(--line); background: var(--surface); color: var(--ink); cursor: pointer; transition: all .18s; min-height: 44px; }
.pick button:hover { border-color: var(--indigo); transform: translateY(-2px); }
.pick button[aria-checked="true"] { background: var(--indigo); border-color: var(--indigo); color: #fff; box-shadow: 0 0 0 3px rgba(135,199,40,.45); }
.pick.days button { display: grid; text-align: center; line-height: 1.15; min-width: 64px; } .pick.days small { font-size: 12px; opacity: .75; }
#demo-form textarea { width: 100%; font: inherit; font-size: 16px; padding: 12px 14px; border-radius: 14px; border: 1px solid var(--line); resize: vertical; }
.hp { position: absolute; left: -9999px; width: 1px; height: 1px; opacity: 0; }
.frow { display: flex; gap: 10px; } .frow .btn { flex: 1; } .btn-ghost { background: transparent; border: 1px solid var(--line); color: var(--ink); }
.linkbtn { background: none; border: 0; font: inherit; cursor: pointer; text-decoration: underline; justify-self: start; color: var(--muted); }
.fok { display: grid; gap: 12px; justify-items: start; padding: 8px 0; animation: fIn .4s ease; }
.fok svg { width: 64px; height: 64px; } .fok circle { fill: var(--lime); } .fok path { fill: none; stroke: var(--indigo-deep); stroke-width: 5; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 40; stroke-dashoffset: 40; animation: draw .6s .25s ease forwards; }
@keyframes draw { to { stroke-dashoffset: 0; } }
.fok h3 { font-size: 26px; font-weight: 500; letter-spacing: -0.03em; } .fok p { color: var(--muted); }
.bk-t { font-size: 22px; font-weight: 500; letter-spacing: -0.03em; color: var(--ink); } .bk-s { color: var(--muted); margin-bottom: 6px; } #f-cal { display: grid; gap: 10px; justify-items: start; }
.fwarn { padding: 12px 14px; border-radius: 14px; background: #FFF4DC; color: #5b4300; font-size: 15px; }
/* floating contact card */
.cc { position: fixed; left: 20px; bottom: 20px; z-index: 58; width: 250px; background: #fff; border: 1px solid var(--line); border-radius: 22px; padding: 18px; display: none; gap: 8px; box-shadow: 0 30px 60px -28px rgba(0,24,74,.5); transform: translateY(24px); opacity: 0; visibility: hidden; transition: all .4s cubic-bezier(.16,1,.3,1); }
.cc.show { transform: none; opacity: 1; visibility: visible; }
@media (min-width: 821px) { .cc { display: grid; } }
.cc b { font-weight: 500; font-size: 17px; color: var(--indigo); } .cc-tel { font-size: 24px; font-weight: 500; letter-spacing: -0.03em; color: var(--ink); text-decoration: none; }
.cc-btn { min-height: 44px; font-size: 15px; justify-content: center; } .cc-mail { font-size: 14px; color: var(--muted); text-decoration: none; }
.cc-x { position: absolute; top: 8px; right: 12px; border: 0; background: none; font-size: 22px; cursor: pointer; color: var(--muted); }
/* walkthrough */
.rp-hint { display: none; margin: 0 0 10px; font-size: 14px; color: rgba(255,255,255,.7); }
@media (max-width: 760px) { .rp-hint { display: block; } }
.wt-inds { margin-top: 26px; display: flex; flex-wrap: wrap; gap: 8px; }
.wt-inds button { font: inherit; font-size: 15px; min-height: 42px; padding: 0 18px; border-radius: 999px; border: 1px solid rgba(255,255,255,.28); background: transparent; color: #fff; cursor: pointer; transition: all .2s; }
.wt-inds button:hover { border-color: rgba(255,255,255,.7); }
.wt-inds button[aria-pressed="true"] { background: var(--lime); border-color: var(--lime); color: var(--indigo-deep); font-weight: 500; }
.wt { background: var(--indigo-deep); color: #fff; }
.wt .eyebrow { color: var(--lime); } .wt .lp-h2 { color: #fff; } .wt .lp-sub { color: rgba(255,255,255,.75); }
.wt-tabs { position: relative; margin-top: 28px; display: inline-flex; gap: 4px; padding: 5px; border-radius: 999px; background: rgba(255,255,255,.1); max-width: 100%; overflow-x: auto; }
.wt-tabs .ind { position: absolute; top: 5px; bottom: 5px; left: 0; width: 0; border-radius: 999px; background: #fff; transition: transform .35s cubic-bezier(.16,1,.3,1), width .35s cubic-bezier(.16,1,.3,1); }
.wt-tabs button { position: relative; z-index: 1; font: inherit; font-size: 16px; font-weight: 500; padding: 11px 20px; border: 0; background: transparent; color: #fff; cursor: pointer; border-radius: 999px; transition: color .25s; min-height: 44px; white-space: nowrap; }
.wt-tabs button[aria-selected="true"] { color: var(--indigo-deep); }
.wt-grid { margin: 30px 0 22px; }
.wt-copy { display: grid; grid-template-columns: 1fr 1fr; gap: 10px 48px; align-items: start; }
.wt-copy h3 { font-size: clamp(26px, 3vw, 38px); font-weight: 500; letter-spacing: -0.04em; line-height: 1.1; grid-column: 1; }
.wt-copy p { font-size: 19px; color: rgba(255,255,255,.8); line-height: 1.45; grid-column: 1; margin: 0; }
.wt-copy ul { grid-column: 2; grid-row: 1 / span 2; margin: 0; padding: 0; list-style: none; display: grid; gap: 10px; align-content: center; } .wt-copy li { display: flex; gap: 10px; color: rgba(255,255,255,.9); font-size: 17px; } .wt-copy li::before { content: ""; flex: none; width: 20px; height: 20px; margin-top: 3px; border-radius: 50%; background: var(--lime) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Cpath d='m5.5 10.5 3 3 6-7' fill='none' stroke='%2300184A' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / contain no-repeat; }
.wt-copy > * { animation: fIn .4s ease both; }
.rp-box { position: relative; }
.toast { position: fixed; z-index: 90; left: 50%; bottom: 30px; transform: translate(-50%, 20px); background: var(--indigo-deep); color: #fff; padding: 12px 20px; border-radius: 999px; opacity: 0; transition: all .3s; font-size: 15px; pointer-events: none; } .toast.on { opacity: 1; transform: translate(-50%, 0); }
.wt-fine { margin-top: 18px; font-size: 14px; color: rgba(255,255,255,.6); }
@media (max-width: 960px) { .wt-copy { grid-template-columns: 1fr; } .wt-copy ul { grid-column: 1; grid-row: auto; } }
@media (max-width: 560px) { .wt-tabs button { padding: 10px 14px; } }
/* reviews */
.rw-grid { margin-top: 44px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
.rw-big { font-size: clamp(56px, 7vw, 92px); font-weight: 200; letter-spacing: -0.06em; line-height: .95; color: var(--accent); } .rw-text { font-size: 21px; line-height: 1.4; color: var(--ink); margin: 0; }
.rw-card { position: relative; margin: 0; background: var(--surface); border: 1px solid var(--line); border-radius: 24px; padding: 28px; display: grid; gap: 22px; align-content: space-between; transition: transform .25s, box-shadow .25s; }
.rw-card:hover { transform: translateY(-6px); box-shadow: 0 30px 60px -34px rgba(0,36,102,.4); }
.rw-card blockquote { margin: 0; font-size: 21px; line-height: 1.4; letter-spacing: -0.01em; color: var(--ink); }
.rw-card figcaption { display: flex; align-items: center; gap: 12px; } .rw-card figcaption b { display: block; font-weight: 500; } .rw-card small { color: var(--muted); font-size: 14px; }
.rw-av { width: 44px; height: 44px; border-radius: 50%; background: var(--indigo); color: var(--lime); display: grid; place-items: center; font-weight: 500; }
.rw-draft { justify-self: start; width: fit-content; font-size: 11.5px; letter-spacing: .06em; text-transform: uppercase; padding: 4px 10px; border-radius: 999px; background: #FFF1D6; color: #8a5a00; }
.rw-badge-unused { position: absolute; top: 16px; right: 16px; font-size: 11.5px; letter-spacing: .08em; text-transform: uppercase; padding: 4px 10px; border-radius: 999px; background: #FFF1D6; color: #8a5a00; }
.rw-card blockquote { font-size: 23px; line-height: 1.38; letter-spacing: -0.01em; }
.rw-note { margin-top: 22px; font-size: 14.5px; color: var(--muted); }
@media (max-width: 960px) { .rw-grid { grid-template-columns: none; grid-auto-flow: column; grid-auto-columns: 88%; overflow-x: auto; scroll-snap-type: x mandatory; padding-bottom: 8px; } .rw-card { scroll-snap-align: start; } }
"""

# ---------------------------------------------------------------- JS
JS = r"""
(function () {
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cfg = { chat: false, email: false };
  fetch('/api/status').then(function (r) { return r.json(); }).then(function (d) { cfg = d; }).catch(function () {});
  function toast(msg) { var t = $('.toast') || document.body.appendChild(Object.assign(document.createElement('div'), { className: 'toast', role: 'status' })); t.textContent = msg; t.classList.add('on'); clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove('on'); }, 2200); }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }

  /* ---- demo form: details, then a preferred time, then email to the team ---- */
  var form = $('#demo-form');
  if (form) {
    var slot = { day: '', time: '' }, TIMES = ['9 to 11 am', '11 am to 1 pm', '1 to 3 pm', '3 to 5 pm'];
    var DN = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], MN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    function show(n) { $$('.fstep', form).forEach(function (s) { s.hidden = s.getAttribute('data-step') !== String(n); }); $$('.fsteps li', form).forEach(function (l) { l.classList.toggle('on', l.getAttribute('data-s') === String(n)); }); }
    function radios(box, items, key) {
      items.forEach(function (it) {
        var b = el('button'); b.type = 'button'; b.setAttribute('role', 'radio'); b.setAttribute('aria-checked', 'false');
        if (it.small) { b.appendChild(el('span', '', it.top)); b.appendChild(el('small', '', it.small)); } else b.textContent = it.top;
        b.addEventListener('click', function () { $$('button', box).forEach(function (x) { x.setAttribute('aria-checked', x === b ? 'true' : 'false'); }); slot[key] = it.value; });
        box.appendChild(b);
      });
    }
    var d = new Date(), days = [];
    if ($('#f-days')) {
    while (days.length < 8) { d.setDate(d.getDate() + 1); if (d.getDay() > 0 && d.getDay() < 6) days.push(new Date(d)); }
    radios($('#f-days'), days.map(function (x) { return { top: DN[x.getDay()] + ' ' + x.getDate(), small: MN[x.getMonth()], value: DN[x.getDay()] + ' ' + x.getDate() + ' ' + MN[x.getMonth()] }; }), 'day');
    radios($('#f-times'), TIMES.map(function (t) { return { top: t, value: t }; }), 'time');
    }

    function valid1() {
      var ok = true; $('#e-name').textContent = ''; $('#e-email').textContent = '';
      if (!$('#f-name').value.trim()) { $('#e-name').textContent = 'Enter your name so we know who to talk to.'; ok = false; }
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test($('#f-email').value)) { $('#e-email').textContent = 'Enter an email like name@business.com.'; ok = false; }
      return ok;
    }
    if ($('#f-next')) $('#f-next').addEventListener('click', function () {
      if (!valid1()) return;
      show(2);
      var link = form.getAttribute('data-book');
      if (link) {
        $('#f-picker').hidden = true; $('#f-back2').hidden = false;
        var cal = $('#f-cal'); cal.hidden = false;
        if (!cal.firstChild) {
          var q = '?embed=true&layout=month_view&name=' + encodeURIComponent($('#f-name').value.trim()) + '&email=' + encodeURIComponent($('#f-email').value.trim());
          cal.appendChild(el('p', 'bk-t', 'Last step: pick a time that works for you.'));
          if (/^https:\/\/cal\.com\//.test(link)) {
            var fr = el('iframe'); fr.src = link + q; fr.title = 'Book a demo time'; fr.loading = 'lazy'; fr.style.cssText = 'width:100%;height:620px;border:0;border-radius:14px;background:#fff'; cal.appendChild(fr);
            var a2 = el('a', 'tlink', 'Open the calendar in a new tab'); a2.href = link + q; a2.target = '_blank'; a2.rel = 'noopener'; cal.appendChild(a2);
          } else {
            cal.appendChild(el('p', 'bk-s', 'The calendar opens in a new tab. You will get a confirmation by email once you book.'));
            var a = el('a', 'btn btn-dark', 'Choose a time'); a.href = link; a.target = '_blank'; a.rel = 'noopener'; cal.appendChild(a);
          }
          // the team gets the contact details even if the visitor never finishes booking
          if (cfg.email) { var typeSel0 = $('#f-type'); fetch('/api/lead', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ kind: 'demo', name: $('#f-name').value.trim(), email: $('#f-email').value.trim(), business: $('#f-practice').value.trim(), phone: $('#f-phone').value.trim(), type: typeSel0.options[typeSel0.selectedIndex].text, notes: 'Reached the booking step. A booking confirmation follows if they pick a time.', page: location.pathname, website: $('#f-website').value }) }).catch(function () {}); }
        }
      }
    });
    if ($('#f-back')) { $('#f-back').addEventListener('click', function () { show(1); }); $('#f-back-cal').addEventListener('click', function () { show(1); }); }
    function done(name, email, when, note) {
      form.textContent = '';
      var w = el('div', 'fok'); w.innerHTML = '<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="30"/><path d="M19 33l9 9 17-20"/></svg>';
      w.appendChild(el('h3', '', 'Thanks, ' + name + '.')); w.appendChild(el('p', '', note || ('We will email ' + email + (when ? ' to confirm ' + when + ' (Eastern).' : ' shortly.'))));
      form.appendChild(w);
    }
    function submit(withTime) {
      var name = $('#f-name').value.trim(), email = $('#f-email').value.trim();
      var when = withTime && slot.day ? slot.day + (slot.time ? ', ' + slot.time : '') : '';
      var typeSel = $('#f-type'), payload = { kind: 'demo', name: name, email: email, business: $('#f-practice').value.trim(), phone: $('#f-phone').value.trim(), type: typeSel.options[typeSel.selectedIndex].text, slot: when ? when + ' ET' : '', notes: $('#f-notes').value, page: location.pathname, website: $('#f-website').value };
      var st = $('#form-status'); st.textContent = '';
      function fallback() {
        var body = 'Name: ' + name + '\nEmail: ' + email + '\nBusiness: ' + payload.business + '\nType: ' + payload.type + '\nPhone: ' + payload.phone + '\nPreferred time: ' + payload.slot + '\nNotes: ' + payload.notes;
        window.location.href = 'mailto:info@member-cloud.com?subject=' + encodeURIComponent('Demo request: ' + (payload.business || name)) + '&body=' + encodeURIComponent(body);
        done(name, email, '', 'The form is not connected to our inbox yet, so I opened an email to info@member-cloud.com with your details. If nothing opened, write to that address or call (888) 408-7007.');
      }
      if (!cfg.email) { fallback(); return; }
      $('#f-send').disabled = true;
      fetch('/api/lead', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(payload) })
        .then(function (r) { if (!r.ok) throw 0; done(name, email, when); })
        .catch(function () { $('#f-send').disabled = false; st.appendChild(el('div', 'fwarn', 'Could not send. Email info@member-cloud.com or call (888) 408-7007.')); });
    }
    form.addEventListener('submit', function (e) { e.preventDefault(); if (form.getAttribute('data-mode') === 'waitlist') { if (valid1()) submit(false); return; } submit(true); });
    if ($('#f-skip')) $('#f-skip').addEventListener('click', function () { submit(false); });
  }

  /* ---- floating contact card ---- */
  var cc = $('#cc');
  if (cc && 'IntersectionObserver' in window) {
    var gone = false; try { gone = sessionStorage.getItem('cc-x') === '1'; } catch (e) {}
    var s = { hero: true, cta: false, wt: false };
    function up() { cc.classList.toggle('show', !gone && !s.hero && !s.cta && !s.wt); }
    if ($('#top')) new IntersectionObserver(function (es) { s.hero = es[0].isIntersecting; up(); }).observe($('#top'));
    var hideOn = $$('#walkthrough, #gpanels'), vis = {};
    hideOn.forEach(function (el, i) { new IntersectionObserver(function (es) { vis[i] = es[0].isIntersecting; s.wt = Object.keys(vis).some(function (k) { return vis[k]; }); up(); }, { threshold: 0.05 }).observe(el); });
    var ctaEl = $('.action'); if (ctaEl) new IntersectionObserver(function (es) { s.cta = es[0].isIntersecting; up(); }, { threshold: 0.05 }).observe(ctaEl);
    $('.cc-x', cc).addEventListener('click', function () { gone = true; try { sessionStorage.setItem('cc-x', '1'); } catch (e) {} up(); });
  }

  /* ---- dashboard walkthrough (replicas of the real product screens) ---- */
  var wt = $('#walkthrough');
  if (wt) {
    var COPY = {
      dashboard: ['See your program at a glance.', 'Active members by plan, current members and members past due, all on one screen.', ['Members by plan, as a chart and a table', 'Current members and members past due', 'No spreadsheets to update']],
      patients: ['Every {p}, one list.', 'Active {P}, failed payments and cancelled {P} in their own lists. Search, sort and export.', ['Add a {s} or upload a file', 'Export to Excel, PDF or CSV, or print', 'Failed payments listed on their own']],
      member: ['Everything about one member.', 'Plan, price, payment method, contract and what the plan includes, in one view.', ['Membership status and dates', 'Contract on file', 'Plan details and what has been used']],
      payments: ['Every payment on record.', 'Invoices, periods and amounts for each subscription cycle.', ['Search and sort the full payment history', 'Invoice and period for every charge', 'Export for reconciliation']],
      landing: ['A page your {P} can enroll from.', 'They choose a plan and enroll from a page with your plans, benefits and answers to common questions.', ['Your plans and prices, clearly laid out', 'Enroll straight from the page', 'Customize it for your business']],
      fees: ['Set the fees for each plan.', 'Add your services and fees, and tailor a fee schedule for each membership plan.', ['Fees you control', 'A schedule for every plan', 'Edit or remove a fee any time']]
    };
    var tabs = $$('.wt-tabs [role=tab]', wt), indEl = $('.wt-tabs .ind', wt), rp = $('.rp', wt), box = $('.rp-box', wt), scroller = $('.rp-scroll', wt), W0 = 1200, H0 = 640, cur = 'dashboard';
    var set = $('.rp-set:not([hidden])', wt);
    function word(s) { var P = set.getAttribute('data-people'), p = P.toLowerCase(); return s.replace(/\{P\}/g, p).replace(/\{p\}/g, p.replace(/s$/, '')).replace(/\{s\}/g, p.replace(/s$/, '')).replace(/^./, function (x) { return x.toUpperCase(); }); }
    function moveInd() { var t = $('[aria-selected=true]', $('.wt-tabs', wt)); if (t && indEl) { indEl.style.width = t.offsetWidth + 'px'; indEl.style.transform = 'translateX(' + t.offsetLeft + 'px)'; } }
    function fit() {
      var w = scroller.clientWidth, s = Math.max(0.5, Math.min(1, w / W0));
      if (window.innerWidth <= 700) { rp.style.zoom = ''; rp.style.transform = 'none'; scroller.scrollLeft = 0; return; }
      /* zoom (not transform: scale) so the browser re-renders text at the final size and it stays sharp */
      rp.style.zoom = s; rp.style.transform = 'none'; box.style.width = ''; box.style.height = '';
      if (W0 * s > w + 1) scroller.scrollLeft = 200 * s; /* small screens: start on the content, not the sidebar */
    }
    function count(node, to) {
      if (reduce) { node.textContent = to; return; }
      var t0 = performance.now(); (function step(t) { var p = Math.min(1, (t - t0) / 900), e = 1 - Math.pow(1 - p, 3); node.textContent = Math.round(to * e); if (p < 1) requestAnimationFrame(step); })(t0);
    }
    function show(k) {
      cur = k; var c = COPY[k];
      $('#wt-h').textContent = word(c[0]); $('#wt-d').textContent = word(c[1]);
      var ul = $('#wt-l'); ul.textContent = ''; c[2].forEach(function (x) { ul.appendChild(el('li', '', word(x))); });
      $$('.wt-copy > *', wt).forEach(function (n) { n.style.animation = 'none'; void n.offsetWidth; n.style.animation = ''; });
      $$('.rp-panel', set).forEach(function (p) { var on = p.getAttribute('data-k') === k; p.hidden = !on; p.classList.remove('go'); if (on) { void p.offsetWidth; p.classList.add('go'); } });
      var pn = $('.rp-panel[data-k=' + k + ']', set);
      $$('.rp-bar', pn).forEach(function (b) { b.style.height = '0'; });
      requestAnimationFrame(function () { requestAnimationFrame(function () { $$('.rp-bar', pn).forEach(function (b) { b.style.height = b.getAttribute('data-h') + '%'; }); }); });
      $$('.rp-num', pn).forEach(function (n) { count(n, +n.getAttribute('data-to')); });
      if (k === 'landing') pn.scrollTop = 0;
      var zs = parseFloat(rp.style.zoom) || 1; if (window.innerWidth > 700) scroller.scrollLeft = (W0 * zs > scroller.clientWidth + 1 && k !== 'landing') ? 200 * zs : 0;
      moveInd();
    }
    tabs.forEach(function (b, i) {
      b.addEventListener('click', function () { tabs.forEach(function (x) { x.setAttribute('aria-selected', x === b ? 'true' : 'false'); x.tabIndex = x === b ? 0 : -1; }); show(b.getAttribute('data-k')); });
      b.addEventListener('keydown', function (e) { var n = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (n) { e.preventDefault(); var t = tabs[(i + n + tabs.length) % tabs.length]; t.focus(); t.click(); } });
    });
    $$('.wt-inds button', wt).forEach(function (bt) {
      bt.addEventListener('click', function () {
        $$('.wt-inds button', wt).forEach(function (x) { x.setAttribute('aria-pressed', x === bt ? 'true' : 'false'); });
        $$('.rp-set', wt).forEach(function (s) { s.hidden = s.getAttribute('data-ind') !== bt.getAttribute('data-ind'); });
        set = $('.rp-set:not([hidden])', wt);
        $('[data-k=patients]', $('.wt-tabs', wt)).textContent = set.getAttribute('data-people');
        $('[data-k=landing]', $('.wt-tabs', wt)).textContent = set.getAttribute('data-page');
        show(cur);
      });
    });
    var drawn = false; function first() { if (drawn) return; drawn = true; show(cur); }
    fit(); window.addEventListener('resize', function () { fit(); moveInd(); }); if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { fit(); moveInd(); });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es, o) { if (es[0].isIntersecting) { first(); o.disconnect(); } }, { threshold: 0.15 }).observe(wt); else first();
    setTimeout(first, 1500);
  }

  /* ---- reveal on scroll for the new blocks ---- */
  if ('IntersectionObserver' in window && !reduce) {
    var rv = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); rv.unobserve(e.target); } }); }, { threshold: 0.15 });
    $$('.rw-card').forEach(function (x, i) { x.classList.add('rv'); x.style.transitionDelay = i * 90 + 'ms'; rv.observe(x); });
  }
})();
"""
