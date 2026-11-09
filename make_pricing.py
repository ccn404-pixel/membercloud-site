"""One-off generator: builds site-v6/pricing.html from the dental landing shell
(head CSS, header, demo form, footer, scripts). Run from anywhere:
  python make_pricing.py
apply_design.py (called by wix-migration/build.py) adds the shared design layer.
"""
from pathlib import Path
import re, sys

SITE = Path(__file__).resolve().parent / 'site-v6'
sys.path.insert(0, str(SITE))
import os
os.chdir(SITE)
from dd import ic

src = (SITE / 'dental.html').read_text()

head, rest = src.split('<main id="main">', 1)
tail = rest[rest.index('<a class="btn btn-dark mcta"'):]

# ---- head: title + meta description
head = re.sub(r'<title>.*?</title>', '<title>MemberCloud Pricing: $149 a Month, Unlimited Admins</title>', head, count=1)
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="One simple price: $149 a month with unlimited admins and locations, '
              'tiered memberships and automated billing. Book a free demo.">', head, count=1)

# ---- header: industries menu without a current page, page-level anchors
head = head.replace(' href="dental.html" aria-current="page"', ' href="dental.html"')
head = re.sub(r'\s*<a href="#benefits">How it helps</a>\s*<a href="#plans">Plan ideas</a>\s*<a href="#pricing">Pricing</a>\s*<a href="#faq">FAQ</a>',
              '\n      <a href="#included">What\'s included</a>\n      <a href="#start">How to start</a>\n      <a href="#faq">FAQ</a>', head, count=1)
assert '#included' in head and 'aria-current' not in head.split('<body>', 1)[1]

PAGE_CSS = """<style>
.pr-card { background: var(--indigo); color: #fff; border-radius: 28px; padding: clamp(28px, 3.4vw, 44px); display: grid; gap: 14px; align-content: start; box-shadow: 0 50px 90px -50px rgba(0,24,74,.55); min-width: 0; }
.pr-card .pr-tag { font-size: 13px; font-weight: 500; letter-spacing: .08em; text-transform: uppercase; color: var(--lime); }
.pr-card .pr-amt { font-size: clamp(52px, 6vw, 84px); font-weight: 500; letter-spacing: -0.045em; line-height: 1; }
.pr-card .pr-amt small { font-size: 20px; font-weight: 400; letter-spacing: 0; margin-left: 6px; color: rgba(255,255,255,.82); }
.pr-card .pr-fine { font-size: 15px; color: rgba(255,255,255,.82); }
.pr-card ul { list-style: none; margin: 10px 0 0; padding: 18px 0 0; border-top: 1px solid rgba(255,255,255,.18); display: grid; gap: 12px; }
.pr-card li { display: flex; gap: 12px; align-items: flex-start; font-size: 18px; line-height: 1.4; }
.pr-card li::before { content: ""; flex: none; width: 20px; height: 20px; margin-top: 3px; border-radius: 50%; background: var(--lime) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2300184A' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 12l5 5 9-10'/%3E%3C/svg%3E") center / 12px no-repeat; }
.pr-grid { margin-top: 48px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
.pr-grid .bcard:last-child { grid-column: span 2; }
.pr-grid .bcard ul { margin: 6px 0 0; padding-left: 20px; color: var(--muted); font-size: 17px; line-height: 1.5; }
.pr-final { text-align: center; }
.pr-final .lp-h2, .pr-final .lp-sub { margin-inline: auto; }
.pr-final .hero-actions2 { justify-content: center; margin-top: 32px; }
@media (max-width: 960px) { .pr-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 560px) { .pr-grid { grid-template-columns: 1fr; } .pr-grid .bcard:last-child { grid-column: auto; } .pr-card li { font-size: 17px; } }
</style>
"""

def card(icon, title, body):
    return f'<div class="bcard"><i>{ic(icon)}</i><h3>{title}</h3>{body}</div>'

cards = ''.join([
    card('users', 'Unlimited admins', '<p>Add as many admins as your team needs.</p>'),
    card('building-store', 'Unlimited locations', '<p>Add every location you run.</p>'),
    card('adjustments-horizontal', 'Tiered memberships', '<p>Set up membership tiers quickly, with your own names, prices and what each plan includes.</p>'),
    card('credit-card', 'Automated billing', '<p>Payments are scheduled, and MemberCloud follows up automatically when a card fails.</p>'),
    card('chart-bar', 'Reporting dashboard', '<ul><li>Active members</li><li>Monthly recurring revenue</li><li>Cancellations</li></ul>'
         '<p>Reports can be exported for reconciliation.</p>'),
])

# Demo form block reused verbatim from the landing pages (same ids, script and cal.com booking).
form = re.search(r'<form id="demo-form"[\s\S]*?</form>', src).group(0)
form = form.replace('<option value="dental" selected>', '<option value="dental">')
contact = re.search(r'<div class="contact">.*?</div>', src).group(0)

FAQ = [
    ('How much does MemberCloud cost?', '$149 a month (introductory pricing for a limited time). It includes unlimited admins, unlimited locations, tiered memberships and automated billing.'),
    ('Is there a free trial?', 'No. The free demo is a live walkthrough with the MemberCloud team, set up around your business so you see your own plans before you decide.'),
    ('Can I customize my plans?', 'Yes. Plan names, pricing, billing frequency, included services, discounts and eligibility rules can be customized. Family and multi-pet plans are possible.'),
    ('What happens when a card fails?', 'Payments are scheduled and MemberCloud follows up automatically when a card fails.'),
    ('Does it replace my practice management or booking software?', 'No. MemberCloud works alongside the system you already use. It does not replace it and it does not sync with it.'),
]
faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)

main = f'''<main id="main">
<section class="lp-hero" id="top">
  <div class="wrap lp-grid">
    <div>
      <h1>One simple price: $149 a month.</h1>
      <p class="lead2">One plan for your membership program, with unlimited admins and locations, tiered memberships and automated billing.</p>
      <div class="hero-actions2">
        <a class="btn btn-ring" href="#demo">Book a free demo <span aria-hidden="true">&rsaquo;</span></a>
        <a class="tlink" href="#included">See what's included</a>
      </div>
      <p class="lp-note">Introductory pricing for a limited time.</p>
    </div>
    <div class="pr-card">
      <span class="pr-tag">MemberCloud</span>
      <div class="pr-amt num">$149<small>/ month</small></div>
      <p class="pr-fine">Introductory pricing for a limited time.</p>
      <ul>
        <li>Unlimited admins</li>
        <li>Unlimited locations</li>
        <li>Tiered memberships, quick to set up</li>
        <li>Automated billing</li>
        <li>Reporting dashboard</li>
      </ul>
    </div>
  </div>
</section>

<section class="lp-sec tint" id="included">
  <div class="wrap">
    <h2 class="lp-h2">What's included.</h2>
    <p class="lp-sub">Everything below comes with the $149 monthly price.</p>
    <div class="pr-grid">{cards}</div>
  </div>
</section>

<section class="lp-sec" id="start">
  <div class="wrap">
    <h2 class="lp-h2">How to get started.</h2>
    <p class="lp-sub">It starts with a free demo: a live meeting with the MemberCloud team, set up around your business.</p>
    <div class="steps"><div class="step"><b>01</b><h3>Book a free demo</h3><p>Pick a time that works for you and meet the MemberCloud team live.</p></div><div class="step"><b>02</b><h3>See your own plans</h3><p>The demo is set up around your business, so you see your own membership plans in MemberCloud.</p></div><div class="step"><b>03</b><h3>Then decide</h3><p>You decide after you have seen how it would work for you.</p></div></div>
  </div>
</section>

<section class="action">
  <img src="real/huddle.jpg" alt="" width="1800" height="1005" loading="lazy">
  <img class="wm" src="images/mark-white.png" alt="" width="600" height="500" loading="lazy">
  <div class="wrap">
    <div class="cta" id="demo">
      <div>
        <h2>Book a free demo.</h2>
        <p class="lead">A live meeting with the MemberCloud team, set up around your business, so you see your own plans before you decide.</p>
        {contact}
      </div>
      {form}
    </div>
  </div>
</section>

<section id="faq">
  <div class="wrap faq-grid">
    <h2>Pricing questions.</h2>
    <div>{faq}</div>
  </div>
</section>

<section class="lp-sec tint pr-final">
  <div class="wrap">
    <h2 class="lp-h2">See MemberCloud with your own plans.</h2>
    <p class="lp-sub">$149 a month. Book a free demo to see how it would work for your business.</p>
    <div class="hero-actions2"><a class="btn btn-dark" href="#demo">Book a free demo</a></div>
  </div>
</section>
'''

head = head.replace('</head><body>', '</head><body>\n' + PAGE_CSS, 1)
out = head + main + tail
(SITE / 'pricing.html').write_text(out)
print('pricing.html', len(out))
