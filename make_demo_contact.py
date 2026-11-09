"""One-off generator: builds site-v6/book-demo.html and site-v6/contact.html from the
dental landing shell (head CSS, header, forms, footer, scripts), same method as make_pricing.py.
  python make_demo_contact.py
apply_design.py (called by wix-migration/build.py) adds the shared design layer.
Facts used come only from the approved KB / existing pages: demo = live meeting, no free trial,
$149/month, (888) 408-7007, info@member-cloud.com.
"""
from pathlib import Path
import re, os

SITE = Path(__file__).resolve().parent
os.chdir(SITE)
src = (SITE / 'dental.html').read_text()
head0, rest = src.split('<main id="main">', 1)
tail0 = rest[rest.index('<a class="btn btn-dark mcta"'):]

CONTACT = re.search(r'<div class="contact">.*?</div>', src).group(0)
DEMO_FORM = re.search(r'<form id="demo-form"[\s\S]*?</form>', src).group(0).replace('<option value="dental" selected>', '<option value="dental">')

NAV_OLD = r'\s*<a href="#benefits">How it helps</a>\s*<a href="#plans">Plan ideas</a>\s*<a href="(?:#pricing|pricing\.html)">Pricing</a>\s*<a href="#faq">FAQ</a>'

PAGE_CSS = """<style>
.pr-card { background: var(--indigo); color: #fff; border-radius: 28px; padding: clamp(28px, 3.4vw, 44px); display: grid; gap: 14px; align-content: start; box-shadow: 0 50px 90px -50px rgba(0,24,74,.55); min-width: 0; }
.pr-card .pr-tag { font-size: 13px; font-weight: 500; letter-spacing: .08em; text-transform: uppercase; color: var(--lime); }
.pr-card .pr-fine { font-size: 16px; color: rgba(255,255,255,.86); line-height: 1.5; }
.pr-card ul { list-style: none; margin: 6px 0 0; padding: 18px 0 0; border-top: 1px solid rgba(255,255,255,.18); display: grid; gap: 12px; }
.pr-card li { display: flex; gap: 12px; align-items: flex-start; font-size: 18px; line-height: 1.4; }
.pr-card li::before { content: ""; flex: none; width: 20px; height: 20px; margin-top: 3px; border-radius: 50%; background: var(--lime) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2300184A' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 12l5 5 9-10'/%3E%3C/svg%3E") center / 12px no-repeat; }
.pr-card .pr-contact { display: grid; gap: 4px; font-size: 20px; }
.pr-card .pr-contact a { color: #fff; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,.4); width: fit-content; }
@media (max-width: 560px) { .pr-card li { font-size: 17px; } }
</style>
"""


def shell(title, desc):
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head0, count=1)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', head, count=1)
    head = head.replace(' href="dental.html" aria-current="page"', ' href="dental.html"')
    assert 'aria-current' not in head.split('<body>', 1)[1]
    return head


def faq_block(items):
    return ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items)


# ------------------------------------------------------------------ DEMO
FAQ = [
    ('Is there a free trial?', 'No. The free demo is a live walkthrough with the MemberCloud team, set up around your business so you see your own plans before you decide.'),
    ('How much does MemberCloud cost?', '$149 a month (introductory pricing for a limited time). It includes unlimited admins, unlimited locations, tiered memberships and automated billing.'),
    ('Does it replace my practice management or booking software?', 'No. MemberCloud works alongside the system you already use. It does not replace it and it does not sync with it.'),
]

head = shell('Book a Free MemberCloud Demo | MemberCloud',
             'Book a free live demo with the MemberCloud team. See your own membership plans, enrollment and automatic billing set up around your business.')
head = re.sub(NAV_OLD, '\n      <a href="#demo">Book a demo</a>\n      <a href="#start">What happens</a>\n      <a href="#faq">FAQ</a>', head, count=1)
assert '#start' in head

main = f'''<main id="main">
<section class="lp-hero" id="top">
  <div class="wrap lp-grid">
    <div>
      <h1>Book your free demo.</h1>
      <p class="lead2">A live meeting with the MemberCloud team, set up around your business, so you see your own membership plans before you decide.</p>
      <div class="hero-actions2">
        <a class="btn btn-ring" href="#demo">Pick a time <span aria-hidden="true">&rsaquo;</span></a>
        <a class="tlink" href="pricing.html">See pricing</a>
      </div>
      <p class="lp-note">$149 a month, introductory pricing for a limited time.</p>
    </div>
    <div class="pr-card">
      <span class="pr-tag">In the demo</span>
      <p class="pr-fine">A live walkthrough, not a recording.</p>
      <ul>
        <li>Your own membership plans in MemberCloud</li>
        <li>Enrollment and automatic billing</li>
        <li>Reports on members and recurring revenue</li>
      </ul>
    </div>
  </div>
</section>

<section class="lp-sec tint" id="start">
  <div class="wrap">
    <h2 class="lp-h2">How it works.</h2>
    <p class="lp-sub">Three steps, and the decision stays with you.</p>
    <div class="steps"><div class="step"><b>01</b><h3>Share your details</h3><p>Tell us your name, email and what kind of business you run.</p></div><div class="step"><b>02</b><h3>Pick a time</h3><p>Choose a slot from the calendar. You get a confirmation by email.</p></div><div class="step"><b>03</b><h3>Meet the team</h3><p>See your own plans in MemberCloud, then decide after you have seen how it would work for you.</p></div></div>
  </div>
</section>

<section class="action">
  <img src="real/huddle.jpg" alt="" width="1800" height="1005" loading="lazy">
  <img class="wm" src="images/mark-white.png" alt="" width="600" height="500" loading="lazy">
  <div class="wrap">
    <div class="cta" id="demo">
      <div>
        <h2>Book a free demo.</h2>
        <p class="lead">Fill in your details, then pick a time that works for you.</p>
        {CONTACT}
      </div>
      {DEMO_FORM}
    </div>
  </div>
</section>

<section id="faq">
  <div class="wrap faq-grid">
    <h2>Before you book.</h2>
    <div>{faq_block(FAQ)}</div>
  </div>
</section>
'''
out = head.replace('</head><body>', '</head><body>\n' + PAGE_CSS, 1) + main + tail0
(SITE / 'book-demo.html').write_text(out)
print('book-demo.html', len(out))

# --------------------------------------------------------------- CONTACT
head = shell('Contact MemberCloud | MemberCloud',
             'Questions about MemberCloud? Send the team a message or write to info@member-cloud.com. To see the product, book a free demo.')
head = re.sub(NAV_OLD, '\n      <a href="#message">Send a message</a>', head, count=1)
head = head.replace('tb-cta" href="#demo"', 'tb-cta" href="book-demo.html"')
assert '#message' in head and 'tb-cta" href="book-demo.html"' in head

CONTACT_FORM = '''<form id="demo-form" data-mode="waitlist" novalidate>
        <div class="fstep" data-step="1">
          <div class="f"><label for="f-name">Your name</label><input id="f-name" type="text" autocomplete="name"><div class="err" id="e-name"></div></div>
          <div class="f"><label for="f-email">Email</label><input id="f-email" type="email" autocomplete="email"><div class="err" id="e-email"></div></div>
          <div class="f"><label for="f-practice">Business name (optional)</label><input id="f-practice" type="text" autocomplete="organization"></div>
          <div class="f"><label for="f-phone">Phone (optional)</label><input id="f-phone" type="tel" autocomplete="tel"></div>
          <select id="f-type" hidden><option value="other" selected>Contact message</option></select>
          <div class="f"><label for="f-notes">How can we help?</label><textarea id="f-notes" rows="4" maxlength="1000"></textarea></div>
          <input class="hp" type="text" id="f-website" tabindex="-1" autocomplete="off" aria-hidden="true">
          <button class="btn btn-dark" type="submit" id="f-send">Send message</button>
        </div>
        <div id="form-status" aria-live="polite"></div>
      </form>'''

main = f'''<main id="main">
<section class="lp-hero" id="top">
  <div class="wrap lp-grid">
    <div>
      <h1>Contact MemberCloud.</h1>
      <p class="lead2">Questions about MemberCloud? Send the team a message and we will reply by email.</p>
      <div class="hero-actions2">
        <a class="btn btn-ring" href="#message">Send a message <span aria-hidden="true">&rsaquo;</span></a>
        <a class="tlink" href="book-demo.html">Or book a free demo</a>
      </div>
    </div>
    <div class="pr-card">
      <span class="pr-tag">Reach us directly</span>
      <div class="pr-contact"><a href="mailto:info@member-cloud.com">info@member-cloud.com</a><a href="tel:+18884087007">(888) 408-7007</a></div>
      <p class="pr-fine">Want to see the product? The free demo is a live meeting with the team, set up around your business.</p>
    </div>
  </div>
</section>

<section class="action">
  <img src="real/huddle.jpg" alt="" width="1800" height="1005" loading="lazy">
  <img class="wm" src="images/mark-white.png" alt="" width="600" height="500" loading="lazy">
  <div class="wrap">
    <div class="cta" id="message">
      <div>
        <h2>Send us a message.</h2>
        <p class="lead">Tell us a little about your business and what you would like to know.</p>
        {CONTACT}
      </div>
      {CONTACT_FORM}
    </div>
  </div>
</section>
'''
tail = tail0.replace('id="mcta" href="#demo">Book a free demo', 'id="mcta" href="book-demo.html">Book a free demo')
# mark contact submissions as such (backend maps kind "contact" to its own email subject)
n = tail.count("kind: 'demo'")
tail = tail.replace("kind: 'demo'", "kind: 'contact'").replace("'Demo request: '", "'Contact message: '")
assert 'id="mcta" href="book-demo.html"' in tail and n >= 1, n
out = head.replace('</head><body>', '</head><body>\n' + PAGE_CSS, 1) + main + tail
(SITE / 'contact.html').write_text(out)
print('contact.html', len(out), 'kind replacements', n)
