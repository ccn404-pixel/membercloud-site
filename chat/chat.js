/* MemberCloud chat widget. Vanilla JS, no dependencies.
   It asks <endpoint>/status (default /api, the Pages Functions on the same site) what is configured:
   - chat: AI replies from chat/kb.js. Otherwise it answers from a small approved FAQ (preview mode).
   - email: "Send this to the team" goes to info@member-cloud.com. Otherwise it offers a mailto link. */
(function () {
  var script = document.currentScript, endpoint = (script && script.getAttribute('data-endpoint')) || '/api';
  var liveChat = false, liveMail = false, history = [], busy = false, handoffShown = false;

  fetch(endpoint + '/status').then(function (r) { return r.json(); }).then(function (d) { liveChat = !!d.chat; liveMail = !!d.email; }).catch(function () {});

  var css = '.mcc{position:fixed;right:20px;bottom:20px;z-index:60;font-family:Outfit,system-ui,sans-serif}' +
    '.mcc *{box-sizing:border-box}.mcc-fab{display:flex;align-items:center;gap:10px;border:0;border-radius:999px;background:#002466;color:#fff;font:500 16px Outfit,system-ui,sans-serif;padding:14px 20px;cursor:pointer;box-shadow:0 18px 40px -16px rgba(0,24,74,.6)}' +
    '.mcc-fab:hover{background:#00184A}.mcc-fab svg{width:22px;height:22px;color:#87C728}' +
    '.mcc-panel{position:absolute;right:0;bottom:64px;width:min(380px,calc(100vw - 32px));height:min(560px,calc(100vh - 120px));background:#fff;border:1px solid #dfe5f0;border-radius:24px;display:none;flex-direction:column;overflow:hidden;box-shadow:0 40px 80px -30px rgba(0,24,74,.5)}' +
    '.mcc.open .mcc-panel{display:flex}.mcc-hd{background:#002466;color:#fff;padding:16px 18px;display:flex;justify-content:space-between;align-items:flex-start;gap:12px}' +
    '.mcc-hd b{display:block;font-weight:500;font-size:17px}.mcc-hd small{display:block;margin-top:3px;font-size:13px;line-height:1.35;color:rgba(255,255,255,.78)}' +
    '.mcc-x{border:0;background:transparent;color:#fff;font-size:26px;line-height:1;cursor:pointer;padding:0 4px}' +
    '.mcc-log{flex:1;overflow:auto;padding:16px;display:flex;flex-direction:column;gap:10px;background:#f6f8fc}' +
    '.mcc-log>*{flex-shrink:0}.mcc-m{max-width:86%;padding:10px 14px;border-radius:18px;font-size:15.5px;line-height:1.45;white-space:pre-wrap;overflow-wrap:anywhere}' +
    '.mcc-m.ma{background:#fff;border:1px solid #e3e8f2;color:#1b2540;align-self:flex-start;border-bottom-left-radius:6px}' +
    '.mcc-m.mu{background:#002466;color:#fff;align-self:flex-end;border-bottom-right-radius:6px}' +
    '.mcc-chips{display:flex;flex-wrap:wrap;gap:8px}.mcc-chips button,.mcc-team{border:1px solid #c9d3e6;background:#fff;color:#002466;border-radius:999px;padding:8px 14px;font:500 14px Outfit,system-ui,sans-serif;cursor:pointer}' +
    '.mcc-chips button:hover,.mcc-team:hover{border-color:#002466}.mcc-team{align-self:flex-start}' +
    '.mcc-form{display:flex;gap:8px;padding:12px;border-top:1px solid #e3e8f2;background:#fff}.mcc-form input{flex:1;min-width:0;border:1px solid #c9d3e6;border-radius:999px;padding:11px 16px;font:16px Outfit,system-ui,sans-serif}' +
    '.mcc-form button{border:0;border-radius:999px;background:#87C728;color:#00184A;font:600 15px Outfit,system-ui,sans-serif;padding:0 18px;cursor:pointer}.mcc-form button:disabled{opacity:.5}' +
    '.mcc-ho{background:#fff;border:1px solid #e3e8f2;border-radius:18px;padding:14px;display:grid;gap:8px}.mcc-ho input,.mcc-ho textarea{width:100%;border:1px solid #c9d3e6;border-radius:12px;padding:10px 12px;font:16px Outfit,system-ui,sans-serif}' +
    '.mcc-ho textarea{min-height:72px;resize:vertical}.mcc-ho button{border:0;border-radius:999px;background:#002466;color:#fff;font:500 15px Outfit,system-ui,sans-serif;padding:11px;cursor:pointer}.mcc-ho .e{color:#b3261e;font-size:14px}.mcc-ho .n{font-size:13px;color:#5a6785}' +
    // Keep the launcher in document flow at narrow effective widths (including
    // browser zoom), so it cannot cover page copy or controls.
    '@media (max-width:1100px){.mcc{position:relative;right:auto;bottom:auto;display:flex;justify-content:flex-end;width:auto;margin:16px 20px}.mcc-fab span{display:none}.mcc-fab{padding:14px}.mcc-panel{position:absolute;right:0;bottom:64px}}' +
    '@media (max-width:820px){.mcc{margin:16px 14px}.mcc-panel{max-height:calc(100dvh - 190px)}}' +
    '@media (max-height:650px){.mcc{position:relative;right:auto;bottom:auto;display:flex;justify-content:flex-end;width:auto;margin:16px 20px}.mcc-panel{position:fixed;right:16px;bottom:16px;height:min(560px,calc(100dvh - 32px))}}' +
    '@media (prefers-reduced-motion:no-preference){.mcc-m{animation:mccIn .25s ease}@keyframes mccIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var root = document.createElement('div'); root.className = 'mcc';
  root.innerHTML = '<button class="mcc-fab" type="button" aria-label="Ask MemberCloud" aria-expanded="false" aria-controls="mcc-panel"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-9 8.3 8.6 8.6 0 0 1-3.6-.8L3 21l1.9-5.3A8.3 8.3 0 0 1 3 11.5 8.5 8.5 0 0 1 12 3a8.5 8.5 0 0 1 9 8.5z"/></svg><span>Ask MemberCloud</span></button>' +
    '<div class="mcc-panel" id="mcc-panel" role="dialog" aria-label="MemberCloud chat"><div class="mcc-hd"><div><b>MemberCloud assistant</b><small>AI-assisted answers. Anything you send to the team is read by a person.</small></div><button class="mcc-x" type="button" aria-label="Close chat">&times;</button></div>' +
    '<div class="mcc-log" role="log" aria-live="polite"></div>' +
    '<form class="mcc-form"><input type="text" aria-label="Your question" placeholder="Ask about plans, pricing, demo..." maxlength="600" autocomplete="off"><button type="submit">Send</button></form></div>';
  document.body.appendChild(root);
  var fab = root.querySelector('.mcc-fab'), log = root.querySelector('.mcc-log'), form = root.querySelector('.mcc-form'), input = form.querySelector('input'), send = form.querySelector('button');

  function add(role, text) { var d = document.createElement('div'); d.className = 'mcc-m ' + (role === 'user' ? 'mu' : 'ma'); d.textContent = text; log.appendChild(d); log.scrollTop = log.scrollHeight; return d; }
  function save() { try { sessionStorage.setItem('mcc', JSON.stringify(history.slice(-20))); } catch (e) {} }
  function toggle(open) { root.classList.toggle('open', open); fab.setAttribute('aria-expanded', open); if (open) { if (!log.children.length) start(); input.focus(); } else fab.focus(); }
  fab.addEventListener('click', function () { toggle(!root.classList.contains('open')); });
  root.querySelector('.mcc-x').addEventListener('click', function () { toggle(false); });
  root.addEventListener('keydown', function (e) { if (e.key === 'Escape') toggle(false); });

  // approved FAQ for preview mode only; live mode uses chat/kb.js on the server
  var FAQ = [
    [/price|cost|how much|\$|pricing|fee/i, 'MemberCloud is $149 a month (introductory pricing for a limited time). It includes unlimited admins, unlimited locations, tiered memberships and automated billing.'],
    [/free|trial|demo/i, 'There is no free trial. The free demo is a live walkthrough with our team, set up around how your business runs, so you can see your own plans before you decide.'],
    [/replace|alongside|integrat|sync|software|pms|booking|pos/i, 'MemberCloud works alongside the software you already use. It does not replace it, and the team can confirm specifics for your setup on a demo call.[[HANDOFF]]'],
    [/where|state|florida|chicago|area|located/i, 'We work anywhere in the United States. We are onboarding practices in South and Central Florida (East Coast) now, with Chicago next.'],
    [/custom|plan|tier|family|discount/i, 'Yes. You can change plan names, pricing, billing frequency, included services, discounts and eligibility rules, and create family or multi-pet plans.'],
    [/hipaa|pci|secur|complian|legal/i, 'I want to be precise on that, so the team will confirm it for you in writing.[[HANDOFF]]'],
    [/dental|vet|gym|yoga|wellness|spa|club/i, 'MemberCloud is built first for dental practices, then veterinary clinics and gyms or wellness studios. Any business that runs memberships can use it.'],
    [/human|person|team|call|quote|contact|email|phone/i, 'Happy to connect you with the team.[[HANDOFF]]']
  ];
  function local(q) { for (var i = 0; i < FAQ.length; i++) if (FAQ[i][0].test(q)) return FAQ[i][1]; return 'I am not sure about that one, so I would rather not guess. I can pass your question to the team.[[HANDOFF]]'; }

  function ask(q) {
    if (!liveChat) return Promise.resolve(local(q));
    return fetch(endpoint + '/chat', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ messages: history }) })
      .then(function (r) { if (!r.ok) throw 0; return r.json(); })
      .then(function (d) { return d.reply + (d.handoff ? '[[HANDOFF]]' : ''); });
  }

  function chips(list) {
    var w = document.createElement('div'); w.className = 'mcc-chips';
    list.forEach(function (t) { var b = document.createElement('button'); b.type = 'button'; b.textContent = t; b.addEventListener('click', function () { w.remove(); say(t); }); w.appendChild(b); });
    log.appendChild(w);
  }
  function start() {
    add('a', 'Hi, I am the MemberCloud assistant. I can answer questions about plans, pricing and the demo.' + (liveChat ? '' : '\n\n(Preview mode: answers come from a short FAQ.)'));
    chips(['How much does it cost?', 'Is there a free trial?', 'Will it replace our software?']);
  }

  function offerTeam() {
    if (handoffShown) return; handoffShown = true;
    var b = document.createElement('button'); b.type = 'button'; b.className = 'mcc-team'; b.textContent = 'Send this to the team';
    b.addEventListener('click', function () { b.remove(); handoffForm(); });
    log.appendChild(b); log.scrollTop = log.scrollHeight;
  }
  function handoffForm() {
    var f = document.createElement('form'); f.className = 'mcc-ho'; f.noValidate = true;
    var lastQ = ''; for (var i = history.length - 1; i >= 0; i--) if (history[i].role === 'user') { lastQ = history[i].content; break; }
    f.innerHTML = '<input name="name" placeholder="Your name" autocomplete="name" aria-label="Your name"><input name="email" type="email" placeholder="Work email" autocomplete="email" aria-label="Work email"><textarea name="message" aria-label="Message for the team"></textarea><div class="e" role="alert"></div><button type="submit">Send to the team</button><div class="n">' + (liveMail ? 'Goes to info@member-cloud.com. We reply by email.' : 'Not connected yet: this opens an email to info@member-cloud.com.') + '</div>';
    f.message.value = lastQ;
    f.addEventListener('submit', function (e) {
      e.preventDefault(); var err = f.querySelector('.e'); err.textContent = '';
      if (!f.name.value.trim()) { err.textContent = 'Add your name.'; return; }
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.email.value)) { err.textContent = 'Enter an email like name@business.com.'; return; }
      if (!f.message.value.trim()) { err.textContent = 'Add a short message.'; return; }
      var ok = function () { f.remove(); add('a', 'Thanks, ' + f.name.value.trim() + '. The team will reply to ' + f.email.value.trim() + '.'); };
      if (!liveMail) {
        location.href = 'mailto:info@member-cloud.com?subject=' + encodeURIComponent('Website chat: ' + f.name.value.trim()) + '&body=' + encodeURIComponent(f.message.value.trim() + '\n\n' + f.name.value.trim() + '\n' + f.email.value.trim());
        f.remove(); add('a', 'I opened an email to info@member-cloud.com for you. If nothing opened, write to that address or call (888) 408-7007.'); return;
      }
      f.querySelector('button').disabled = true;
      fetch(endpoint + '/lead', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ kind: 'chat', name: f.name.value, email: f.email.value, message: f.message.value, page: location.pathname, transcript: history }) })
        .then(function (r) { if (!r.ok) throw 0; ok(); })
        .catch(function () { f.querySelector('button').disabled = false; err.textContent = 'Could not send. Email info@member-cloud.com or call (888) 408-7007.'; });
    });
    log.appendChild(f); log.scrollTop = log.scrollHeight; f.name.focus();
  }

  function say(q) {
    if (busy || !q.trim()) return; busy = true; send.disabled = true;
    add('user', q); history.push({ role: 'user', content: q }); input.value = '';
    var wait = add('a', '...');
    ask(q).then(function (a) {
      var h = /\[\[HANDOFF\]\]/.test(a); a = a.replace('[[HANDOFF]]', '').trim();
      wait.textContent = a; history.push({ role: 'assistant', content: a }); save(); if (h) offerTeam();
    }).catch(function () {
      wait.textContent = 'Something went wrong. You can email info@member-cloud.com or call (888) 408-7007.'; offerTeam();
    }).then(function () { busy = false; send.disabled = false; input.focus(); });
  }
  form.addEventListener('submit', function (e) { e.preventDefault(); say(input.value); });
})();
