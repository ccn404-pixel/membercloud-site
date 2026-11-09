#!/usr/bin/env python3
"""Builds one landing page per industry from the approved copy and design of membercloud-site.html.
Run from site-v6/:  python3 build_landings.py
Outputs: dental.html, veterinary.html, gym-wellness.html, any-membership.html
Mental health is intentionally not built until the legal review is done (Edgar call, 19 Oct 2026).
"""
import math, re, html, os, sys
sys.path.insert(0, '.')  # run with -I, so add this folder for dd.py
from dd import ic, dd_html, DD_CSS, DD_JS
from blocks import CSS as BCSS, JS as BJS, form_html, walkthrough_html, reviews_html, contact_card_html

SRC = open('membercloud-site.html', encoding='utf-8').read()
BASE_CSS = SRC.split('<style>', 1)[1].split('</style>', 1)[0]

LP_CSS = """
/* landing pages */
.lp-hero { position: relative; padding: clamp(40px, 6vw, 88px) 0 clamp(56px, 7vw, 104px); overflow: hidden; }
.lp-grid { display: grid; grid-template-columns: 1.1fr .9fr; gap: clamp(32px, 5vw, 80px); align-items: center; }
.lp-hero h1 { margin-top: 0; font-size: clamp(38px, 5vw, 68px); font-weight: 500; line-height: 1.02; letter-spacing: -0.045em; color: var(--indigo); text-wrap: balance; }
.lp-hero .lead2 { margin-top: 22px; max-width: 30em; }
.lp-hero .hero-actions2 { justify-content: flex-start; }
.lp-note { margin-top: 18px; font-size: 14px; color: var(--muted); }
.lp-media { position: relative; border-radius: 28px; overflow: hidden; aspect-ratio: 4 / 4.7; background: var(--indigo); box-shadow: 0 50px 90px -50px rgba(0,24,74,.55); }
.lp-media img, .lp-media video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.lp-chip { position: absolute; top: 18px; right: 18px; background: #fff; border-radius: 999px; padding: 9px 16px; font-size: 14px; font-weight: 500; color: var(--ink); }
.lp-sec { padding-block: clamp(64px, 8vw, 120px); }
.lp-h2 { margin-top: 14px; color: var(--indigo); font-weight: 500; letter-spacing: -0.045em; max-width: 15em; }
.lp-sub { margin-top: 16px; color: var(--muted); max-width: 34em; font-size: 20px; }
.bgrid { margin-top: 48px; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; }
.bcard { border: 1px solid var(--line); border-radius: 24px; padding: 28px; background: var(--surface); display: grid; gap: 10px; align-content: start; }
.bcard:first-child { background: var(--indigo); border-color: var(--indigo); color: #fff; }
.bcard:first-child p { color: rgba(255,255,255,.82); }
.bcard i { font-style: normal; width: 36px; height: 36px; border-radius: 50%; background: var(--lime); color: var(--indigo-deep); display: grid; place-items: center; font-weight: 600; font-size: 16px; }
.bcard h3 { font-size: 23px; font-weight: 500; letter-spacing: -0.03em; line-height: 1.15; }
.bcard p { font-size: 17px; color: var(--muted); line-height: 1.45; }
.ex-grid { margin-top: 48px; display: grid; grid-template-columns: 1fr 1fr; gap: clamp(24px, 4vw, 56px); align-items: stretch; }
.plan-card { background: var(--mint-soft); border-radius: 28px; padding: clamp(28px, 3.4vw, 44px); display: grid; gap: 12px; align-content: start; }
.plan-card .tag { font-size: 13px; font-weight: 500; letter-spacing: .08em; text-transform: uppercase; color: var(--lime-text); }
.plan-card b { font-size: clamp(34px, 4vw, 52px); font-weight: 500; letter-spacing: -0.04em; color: var(--indigo); line-height: 1.05; }
.plan-card p { font-size: 19px; color: var(--ink-2); max-width: 24em; }
.math-card { background: var(--indigo-deep); color: #fff; border-radius: 28px; padding: clamp(28px, 3.4vw, 44px); display: grid; gap: 6px; align-content: start; }
.math-card .row { display: flex; justify-content: space-between; align-items: baseline; gap: 16px; padding: 16px 0; border-top: 1px solid rgba(255,255,255,.16); }
.math-card .row:first-of-type { border-top: 0; }
.math-card span { font-size: 17px; color: rgba(255,255,255,.82); }
.math-card strong { font-size: clamp(26px, 3vw, 38px); font-weight: 500; letter-spacing: -0.03em; color: var(--lime); font-variant-numeric: tabular-nums; }
.math-card .fine { color: rgba(255,255,255,.62); margin-top: 8px; font-size: 14px; }
.proof-lp { background: var(--bg); border-radius: 28px; padding: clamp(28px, 4vw, 56px); display: grid; grid-template-columns: 1.1fr .9fr; gap: clamp(24px, 4vw, 64px); align-items: center; }
.proof-lp .big { font-size: clamp(64px, 9vw, 120px); font-weight: 200; letter-spacing: -0.06em; line-height: .95; color: var(--accent); }
.proof-lp p { margin-top: 14px; font-size: 22px; color: var(--ink-2); max-width: 22em; line-height: 1.4; }
.proof-lp cite { display: block; margin-top: 14px; font-style: normal; font-size: 15px; color: var(--muted); }
.proof-lp .pimg { border-radius: 24px; overflow: hidden; aspect-ratio: 4 / 4.4; }
.proof-lp .pimg img { width: 100%; height: 100%; object-fit: cover; }
.proof-lp.solo { grid-template-columns: 1fr; }
.steps { margin-top: 48px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
.step { border-top: 1px solid var(--ink); padding-top: 20px; display: grid; gap: 10px; align-content: start; }
.step b { font-size: 15px; font-weight: 500; color: var(--lime-text); letter-spacing: .08em; }
.step h3 { font-size: 26px; font-weight: 500; letter-spacing: -0.03em; }
.step p { color: var(--muted); font-size: 18px; }
.others { margin-top: 28px; display: flex; flex-wrap: wrap; gap: 10px; }
.others a { text-decoration: none; padding: 14px 22px; border: 1px solid var(--line); border-radius: 999px; background: var(--surface); font-weight: 500; color: var(--ink); transition: border-color .2s, transform .2s; }
.others a:hover { border-color: var(--indigo); transform: translateY(-2px); }
.tiers { margin-top: 48px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
.tier { border: 1px solid var(--line); border-radius: 24px; padding: 28px; background: var(--surface); display: grid; gap: 8px; align-content: start; }
.tier .tn { font-size: 15px; font-weight: 500; letter-spacing: .08em; text-transform: uppercase; color: var(--lime-text); }
.tier b { font-size: clamp(32px, 3.4vw, 44px); font-weight: 500; letter-spacing: -0.04em; color: var(--indigo); line-height: 1.05; }
.tier b small { font-size: 16px; font-weight: 400; color: var(--muted); letter-spacing: 0; margin-left: 6px; }
.tier p { font-size: 18px; color: var(--ink-2); line-height: 1.45; }
.chips { margin-top: 28px; display: flex; flex-wrap: wrap; gap: 8px; }
.chips span { padding: 9px 16px; border-radius: 999px; background: var(--mint-soft); color: var(--indigo); font-size: 15px; font-weight: 500; }
.chips-src { margin-top: 14px; font-size: 14px; color: var(--muted); }
.ic { width: 1em; height: 1em; display: block; }
.bcard i svg { width: 20px; height: 20px; }
.lp-chip { display: inline-flex; align-items: center; gap: 8px; } .lp-chip .ic { width: 18px; height: 18px; color: var(--indigo); }
button.tier { font: inherit; text-align: left; cursor: pointer; color: inherit; transition: border-color .2s, transform .2s, box-shadow .2s; }
button.tier:hover { transform: translateY(-3px); border-color: var(--indigo); }
button.tier[aria-pressed="true"] { border-color: var(--lime); box-shadow: 0 0 0 2px var(--lime) inset; background: var(--mint-soft); }
.tier .ti { width: 44px; height: 44px; border-radius: 14px; background: var(--indigo); color: var(--lime); display: grid; place-items: center; margin-bottom: 8px; }
.tier .ti svg { width: 24px; height: 24px; }
.plan-card { align-content: center; }
.tier .pick { text-align: left; margin-top: 6px; font-size: 14px; color: var(--muted); }
.calc { margin-top: 10px; display: grid; gap: 14px; }
.calc label { display: flex; justify-content: space-between; gap: 12px; font-size: 16px; color: rgba(255,255,255,.82); }
.calc label output { color: #fff; font-weight: 500; font-variant-numeric: tabular-nums; }
.calc input[type=range] { width: 100%; accent-color: var(--lime); height: 28px; }
.rv { opacity: 0; transform: translateY(18px); transition: opacity .6s ease, transform .6s ease; }
.rv.in { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) { .rv { opacity: 1; transform: none; transition: none; } }
.lp-sec.tint { background: var(--surface); border-block: 1px solid var(--line); }
@media (max-width: 960px) { .lp-grid, .ex-grid, .proof-lp { grid-template-columns: 1fr; } .bgrid { grid-template-columns: repeat(2, minmax(0, 1fr)); } .tiers { grid-template-columns: 1fr; } .steps { grid-template-columns: 1fr; } .lp-media { max-width: 560px; } }
@media (max-width: 560px) { .bgrid { grid-template-columns: 1fr; } .math-card .row { flex-direction: column; gap: 4px; } }
"""

# shared FAQ answers (all already approved on the home page)
FAQ = {
    'alongside': ('Does MemberCloud replace our {sw}?', 'No. It works alongside your existing practice management, booking or POS system and focuses on memberships, payments and reporting. Reports can be exported for reconciliation.'),
    'custom': ('Can we customize our membership plans?', 'Yes. You can change plan names, pricing, billing frequency, included services, discounts and eligibility rules, and create family or multi-pet plans.'),
    'trial': ('Is there a free trial?', 'Not at the moment. The free demo is a live walkthrough with our team, set up around how your business runs, so you can see your own plans before you decide. After that, MemberCloud is $149 a month.'),
    'where': ('Where do you work?', 'Anywhere in the United States. Our first clients are dental practices in Florida, and we are currently onboarding practices in South and Central Florida (East Coast), with Chicago next.'),
}

PAGES = [
    dict(
        slug='dental', file='dental.html', form='dental', label='Dental practices',
        title='Dental membership plans, run on autopilot | MemberCloud',
        desc='Run in-house dental membership plans for patients without insurance. MemberCloud handles enrollment, billing and renewals.',
        h1='Dental membership plans, run on autopilot.',
        lead='Offer in-house plans to patients without insurance. MemberCloud handles enrollment, billing and renewals so your front desk does not have to.',
        media=('video', 'real/v-dental.mp4', 'real/p-dental.jpg', 'A hygienist and a patient laughing together in a modern dental studio at dusk'),
        who='dental practice', sw='practice management software',
        h2='How MemberCloud helps dental practices.',
        sub='Package preventative care, perio maintenance and discounts on treatment into plans patients understand at a glance.',
        benefits=[('Set the plan', 'Set a monthly or yearly price and what each plan includes.'),
                  ('Enroll in a few clicks', 'Enroll patients and check eligibility in a few clicks, with almost no training for the front desk.'),
                  ('Automated billing', 'Scheduled payments and automatic follow-up when a card fails. Your staff stops chasing members.'),
                  ('Clear reporting', 'Track active members, recurring revenue and cancellations in one dashboard instead of spreadsheets.')],
        plan=('Example plan', '$35 / month', '2 cleanings and 2 exams, fluoride and X-rays, 1 emergency exam, 10 to 20% off other treatments.'),
        fee=35, members=60, member_word='members',
        icon='dental', bicons=['adjustments-horizontal', 'user-plus', 'credit-card', 'chart-bar'], ticons=['dental', 'mood-kid', 'heart-rate-monitor'],
        tiers_h='Plan ideas for a dental practice.', tiers_sub='Most practices start with one adult plan, then add a children plan and a periodontal maintenance plan.',
        tiers=[('Adult preventive', '$35', '2 cleanings and 2 exams, fluoride and X-rays, 10 to 20% off other treatment.'),
               ('Children', '$25', '2 cleanings and 2 exams, fluoride, and a discount on sealants.'),
               ('Perio maintenance', '$59', 'Periodontal maintenance visits through the year, exams and X-rays, a discount on treatment.')],
        proof=dict(kind='case', big='+40%', text='more affiliated patients in 3 months at Stuart Pediatric Dentistry, a dental practice running on MemberCloud.', cite='Reported by the practice', img=('real/dental-family.jpg', 'A father and his daughter at the front desk of a pediatric dental office'),
                   ctx='About a quarter of US dentists already offer in-house plans (2021 ADA survey, reported by KFF Health News).'),
        extra_faq=[('Is it secure for a dental practice?', 'For dental practices, MemberCloud is PCI and HIPAA compliant.')],
    ),
    dict(
        slug='veterinary', file='veterinary.html', form='veterinary', label='Veterinary and pet care',
        title='Pet wellness plans for veterinary clinics | MemberCloud',
        desc='Offer pet wellness plans that keep owners coming back. One account per household, payments and renewals on autopilot.',
        h1='Pet wellness plans that keep owners coming back.',
        lead='Manage multi-pet households under one account, track included visits and services, and let MemberCloud keep payments and renewals on autopilot.',
        media=('video', 'real/v-vet.mp4', 'real/p-vet.jpg', 'A veterinarian greeting a golden retriever while the owner smiles'),
        who='clinic', sw='practice or booking software',
        h2='How MemberCloud helps veterinary clinics.',
        sub='Turn one-off visits into a plan owners are glad to keep.',
        benefits=[('One account per household', 'One account for every pet in the household, with family and multi-pet plans.'),
                  ('Included visits', 'Track the visits and services each plan includes.'),
                  ('Payments on their own', 'Payments and renewals run on their own, with automatic follow-up when a card fails.'),
                  ('Clear reporting', 'Active members, monthly recurring revenue and cancellations in clean dashboards.')],
        plan=('Example plan', '$34 / month', 'Wellness exam for every pet, core vaccines included, one account for the whole household.'),
        fee=34, members=60, member_word='households',
        icon='paw', bicons=['paw', 'stethoscope', 'credit-card', 'chart-bar'], ticons=['bone', 'dog', 'heart'],
        tiers_h='Plan ideas for a veterinary clinic.', tiers_sub='Plans that follow the life of the pet, with one account for the household.',
        tiers=[('Puppy and kitten', '$29', 'Wellness exams and the first-year vaccines in one monthly price.'),
               ('Adult wellness', '$34', 'Annual wellness exam, core vaccines and a discount on other services.'),
               ('Senior care', '$44', 'Two exams a year, annual bloodwork and a discount on diagnostics.')],
        proof=dict(kind='stat', big='14 to 27%', text='of US clinics offer wellness plans in published surveys, so most clinics still have none.', cite='Published industry surveys'),
        extra_faq=[('Can I set up one plan for a household with several pets?', 'Yes. You can create family or multi-pet plans and keep every pet under one account.')],
    ),
    dict(
        slug='gym-wellness', file='gym-wellness.html', form='gym', label='Gyms and wellness',
        title='Membership software for gyms and wellness studios | MemberCloud',
        desc='Create clear tiers, automate recurring dues and see which plans bring the most loyal members.',
        h1='Memberships for gyms and wellness studios, without the spreadsheets.',
        lead='Simplify access to memberships for fitness studios, yoga, pilates and wellness clubs. Create clear tiers and automate recurring dues.',
        media=('image', 'real/yoga.jpg', None, 'A yoga instructor adjusting a student’s posture in a sunlit studio'),
        who='studio', sw='booking or POS system',
        h2='How MemberCloud helps gyms and wellness clubs.',
        sub='See which plans drive the most loyal, high-value members.',
        benefits=[('Clear tiers', 'Clear tiers for classes, access and packages, with the plan names and prices you choose.'),
                  ('Dues on autopilot', 'Recurring dues collected automatically, with follow-up when a card fails.'),
                  ('Know your best plans', 'See which plans bring the most loyal members.'),
                  ('Clear reporting', 'Active members, monthly recurring revenue and cancellations in one place.')],
        plan=('Example plan', '$89 / month', 'Unlimited classes, one guest pass a month, member pricing on workshops.'),
        fee=89, members=100, member_word='members',
        icon='barbell', bicons=['stretching', 'credit-card', 'heartbeat', 'chart-bar'], ticons=['barbell', 'yoga', 'stretching'],
        tiers_h='Plan ideas for a gym or studio.', tiers_sub='Build tiers around the training types you teach and the areas of the floor you offer. Categories and equipment below come from an open exercise dataset.',
        tiers=[('Strength floor', '$49', 'Open access to the weight floor and member pricing on workshops.'),
               ('Studio unlimited', '$89', 'Unlimited classes, one guest pass a month, member pricing on workshops.'),
               ('Mobility and recovery', '$59', 'Stretching and mobility classes plus the foam roll and bands area.')],
        chips=['Strength', 'Stretching', 'Plyometrics', 'Cardio', 'Powerlifting', 'Olympic weightlifting', 'Strongman', 'Barbell', 'Dumbbell', 'Kettlebells', 'Bands', 'Medicine ball', 'Exercise ball', 'Foam roll'],
        proof=dict(kind='stat', big='77 million', text='Americans held a gym membership in 2024.', cite='L.E.K. Consulting'),
        extra_faq=[('Can I offer different membership tiers?', 'Yes. You can change plan names, pricing, billing frequency and included services, and set discounts and eligibility rules.')],
    ),
    dict(
        slug='any-membership', file='any-membership.html', form='other', label='Any membership business',
        title='Membership software for clubs, med spas and local businesses | MemberCloud',
        desc='Clubs, med spas and local service businesses that run memberships, packages or recurring dues can use MemberCloud too.',
        h1='Any business that sells a membership, in one place.',
        lead='Clubs, med spas and local service businesses that run memberships, packages or recurring dues can use MemberCloud too. Tell us how yours works and we will show you your plan in a demo.',
        media=('image', 'real/studio.jpg', None, 'A studio owner chatting with a regular member at the front counter in the evening'),
        who='business', sw='booking or POS system',
        h2='How MemberCloud helps membership businesses.',
        sub='Your plans, your prices, your rules.',
        benefits=[('Your plans, your way', 'Change plan names, pricing, billing frequency and included services.'),
                  ('Rules and discounts', 'Set discounts and eligibility rules, and create family or multi-pet plans.'),
                  ('Automated billing', 'Scheduled payments and automatic follow-up when a card fails.'),
                  ('Reports you can export', 'Active members, recurring revenue and cancellations, with reports exported for reconciliation.')],
        plan=('Example plan', '$60 / month', 'A simple monthly membership with the benefits and discounts you decide.'),
        fee=60, members=50, member_word='members',
        icon='building-store', bicons=['adjustments-horizontal', 'users-group', 'credit-card', 'chart-bar'], ticons=['user', 'users', 'users-group'],
        tiers_h='Plan ideas for any membership.', tiers_sub='A simple ladder works for clubs, med spas and local service businesses.',
        tiers=[('Basic', '$30', 'The core benefit, billed monthly.'),
               ('Plus', '$60', 'More visits or services each month, plus member pricing.'),
               ('Family', '$90', 'Plus benefits shared by the household.')],
        proof=None,
        extra_faq=[('What kinds of businesses can use MemberCloud?', 'Any business that runs memberships, plans, packages or recurring dues: clubs, med spas, gyms, wellness studios, veterinary clinics, dental and medical practices and local service businesses.')],
    ),
    dict(
        slug='mental-health', file='mental-health.html', form='mental', label='Mental health practices', soon=True,
        title='Membership plans for mental health practices, coming soon | MemberCloud',
        desc='MemberCloud is preparing membership plan management for mental health practices. Join the waitlist.',
        h1='Membership plans for mental health practices, coming soon.',
        lead='We are getting MemberCloud ready for mental health practices. Join the waitlist and we will email you when it opens.',
        media=('video', 'real/v-mental.mp4', 'real/p-mental.jpg', 'A quiet therapy room at golden hour with two armchairs'),
        who='practice', sw='practice management or booking software',
        h2='What MemberCloud will bring to mental health practices.',
        sub='The same simple membership tools, set up around how your practice works.',
        benefits=[('Plans you define', 'Set the price, billing frequency and what each plan includes.'),
                  ('Automated billing', 'Scheduled payments and automatic follow-up when a card fails.'),
                  ('Clear reporting', 'Active members, recurring revenue and cancellations in one dashboard.'),
                  ('Opening soon', 'We are finalizing the details for this industry with care, so it is ready when you are.')],
        icon='mood-smile', bicons=['adjustments-horizontal', 'credit-card', 'chart-bar', 'heart'], ticons=[], tiers=[], plan=('', '', ''), fee=1, members=1, member_word='members',
        tiers_h='', tiers_sub='', proof=None,
        extra_faq=[('When will it open for mental health practices?', 'We are preparing it now. Join the waitlist and we will email you as soon as it is ready.')],
    ),
]

WT = {'dental': 'dental', 'veterinary': 'veterinary', 'gym-wellness': 'gym', 'any-membership': 'any', 'mental-health': 'any'}
TYPES = [('dental', 'Dental practice'), ('veterinary', 'Veterinary clinic'), ('gym', 'Gym or wellness club'), ('mental', 'Mental health practice'), ('other', 'Something else')]
money = lambda n: '${:,.0f}'.format(n)
esc = html.escape


def media_html(p):
    kind, src, poster, alt = p['media']
    if kind == 'video':
        v = f'<video src="{src}" poster="{poster}" autoplay muted loop playsinline preload="metadata" aria-label="{esc(alt)}"></video>'
    else:
        v = f'<img src="{src}" alt="{esc(alt)}" width="1120" height="1500">'
    return f'<div class="lp-media">{v}<span class="lp-chip">{ic(p["icon"])}{esc(p["label"])}</span></div>'


def proof_html(p):
    pr = p['proof']
    if not pr:
        return ''
    ctx = f'<p class="ctx" style="margin-top:18px">{esc(pr["ctx"])}</p>' if pr.get('ctx') else ''
    left = f'<div><div class="big num">{esc(pr["big"])}</div><p>{esc(pr["text"])}</p><cite>{esc(pr["cite"])}</cite>{ctx}</div>'
    if pr['kind'] == 'case':
        right = f'<div class="pimg"><img src="{pr["img"][0]}" alt="{esc(pr["img"][1])}" width="1120" height="1500" loading="lazy"></div>'
        return f'<section class="lp-sec"><div class="wrap"><div class="proof-lp">{left}{right}</div></div></section>'
    return f'<section class="lp-sec"><div class="wrap"><div class="proof-lp solo">{left}</div></div></section>'


STEPS = [('Book a demo', 'A live walkthrough with our team, set up around how your {who} runs.'), ('Build your plans', 'Set the price, billing frequency and what each plan includes.'), ('Enroll and run', 'Enroll members. Payments, renewals and reporting run in one dashboard.')]
STEPS_SOON = [('Join the waitlist', 'Leave your details so we know your practice.'), ('We keep you posted', 'You get an email as soon as MemberCloud opens for mental health.'), ('Book a demo', 'A live walkthrough with our team, set up around how your practice runs.')]


MH_CSS = """
/* mental health: coming soon page */
.mh-hero { padding: clamp(36px, 5vw, 72px) 0 clamp(48px, 6vw, 96px); }
.mh-grid { display: grid; grid-template-columns: 1.05fr .95fr; gap: clamp(32px, 5vw, 80px); align-items: center; }
.mh-badge { display: inline-flex; align-items: center; gap: 10px; padding: 8px 16px 8px 12px; border-radius: 999px; background: #FFF4DC; color: #6B4A00; font-size: 14px; font-weight: 500; letter-spacing: .02em; }
.mh-badge i { width: 9px; height: 9px; border-radius: 50%; background: #E0A100; box-shadow: 0 0 0 0 rgba(224,161,0,.5); animation: mhPulse 2s infinite; }
@keyframes mhPulse { 70% { box-shadow: 0 0 0 10px rgba(224,161,0,0); } 100% { box-shadow: 0 0 0 0 rgba(224,161,0,0); } }
.mh-hero h1 { margin-top: 22px; font-size: clamp(40px, 5.4vw, 74px); font-weight: 500; line-height: 1.02; letter-spacing: -0.045em; color: var(--indigo); text-wrap: balance; }
.mh-hero h1 em { font-style: normal; color: var(--accent); }
.mh-hero .lead2 { margin-top: 22px; max-width: 29em; }
.mh-hero .hero-actions2 { justify-content: flex-start; margin-top: 30px; }
.mh-media { position: relative; margin: 0; border-radius: 32px; overflow: hidden; aspect-ratio: 4 / 4.6; background: var(--indigo); box-shadow: 0 50px 90px -50px rgba(0,24,74,.55); }
.mh-media video, .mh-media img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.mh-media figcaption { position: absolute; left: 18px; right: 18px; bottom: 18px; background: rgba(255,255,255,.92); backdrop-filter: blur(8px); border-radius: 18px; padding: 14px 18px; display: flex; align-items: center; gap: 12px; font-size: 15px; color: var(--ink); }
.mh-media figcaption span { width: 38px; height: 38px; flex: none; border-radius: 12px; background: var(--indigo); color: var(--lime); display: grid; place-items: center; } .mh-media figcaption svg { width: 20px; height: 20px; }
.mh-sec { padding-block: clamp(64px, 8vw, 112px); }
.mh-cards { margin-top: 44px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
.mh-card { background: var(--surface); border: 1px solid var(--line); border-radius: 24px; padding: 30px; display: grid; gap: 12px; align-content: start; transition: transform .25s, box-shadow .25s; }
.mh-card:hover { transform: translateY(-4px); box-shadow: 0 30px 60px -36px rgba(0,36,102,.35); }
.mh-card i { width: 48px; height: 48px; border-radius: 14px; background: var(--mint-soft); color: var(--accent); display: grid; place-items: center; } .mh-card i svg { width: 24px; height: 24px; }
.mh-card h3 { font-size: 24px; font-weight: 500; letter-spacing: -0.03em; } .mh-card p { color: var(--muted); font-size: 17px; line-height: 1.5; }
.mh-band { position: relative; border-radius: 32px; overflow: hidden; min-height: 420px; display: grid; align-items: end; color: #fff; }
.mh-band img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.mh-band::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(0,24,74,.92) 0%, rgba(0,24,74,.7) 45%, rgba(0,24,74,.1) 100%); }
.mh-band div { position: relative; z-index: 1; padding: clamp(28px, 5vw, 64px); max-width: 640px; }
.mh-band h2 { font-size: clamp(30px, 3.6vw, 48px); font-weight: 500; letter-spacing: -0.04em; line-height: 1.08; } .mh-band p { margin-top: 14px; font-size: 19px; color: rgba(255,255,255,.82); line-height: 1.5; }
.mh-steps { margin-top: 44px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; counter-reset: s; }
.mh-step { position: relative; padding: 28px; border-radius: 24px; background: var(--bg); display: grid; gap: 10px; align-content: start; }
.mh-step b { width: 40px; height: 40px; border-radius: 50%; background: var(--indigo); color: var(--lime); display: grid; place-items: center; font-weight: 500; }
.mh-step h3 { font-size: 22px; font-weight: 500; letter-spacing: -0.02em; } .mh-step p { color: var(--muted); font-size: 17px; }
.mh-wait { background: var(--indigo-deep); color: #fff; border-radius: 32px; padding: clamp(28px, 5vw, 64px); display: grid; grid-template-columns: 1fr 1fr; gap: clamp(28px, 5vw, 72px); align-items: center; position: relative; overflow: hidden; }
.mh-wait::before { content: ""; position: absolute; width: 420px; height: 420px; border-radius: 50%; right: -120px; top: -160px; background: radial-gradient(circle, rgba(135,199,40,.35), transparent 65%); }
.mh-wait > * { position: relative; }
.mh-wait h2 { font-size: clamp(32px, 4vw, 52px); font-weight: 500; letter-spacing: -0.04em; line-height: 1.05; } .mh-wait p { margin-top: 14px; color: rgba(255,255,255,.8); font-size: 19px; line-height: 1.5; }
.mh-wait .contact { margin-top: 26px; display: grid; gap: 6px; color: rgba(255,255,255,.85); }
.mh-form { background: #fff; color: var(--ink); border-radius: 24px; padding: clamp(22px, 3vw, 34px); }
.mh-form h3 { font-size: 22px; font-weight: 500; letter-spacing: -0.02em; margin-bottom: 16px; color: var(--indigo); }
.mh-more { margin-top: 28px; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; } .mh-more span { color: var(--muted); margin-right: 4px; }
.mh-more a { text-decoration: none; padding: 12px 20px; border: 1px solid var(--line); border-radius: 999px; background: var(--surface); font-weight: 500; color: var(--ink); transition: border-color .2s, transform .2s; } .mh-more a:hover { border-color: var(--indigo); transform: translateY(-2px); }
@media (max-width: 960px) { .mh-grid, .mh-wait { grid-template-columns: 1fr; } .mh-cards, .mh-steps { grid-template-columns: 1fr; } .mh-media { max-width: 560px; } }
"""


def soon_main(p, faq_html, others):
    kind, src, poster, alt = p['media']
    cards = ''.join(f'<div class="mh-card"><i>{ic(p["bicons"][i])}</i><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, (t, d) in enumerate(p['benefits'][:3]))
    steps = ''.join(f'<div class="mh-step"><b>{i + 1}</b><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, (t, d) in enumerate(STEPS_SOON))
    return f"""
<section class="mh-hero" id="top">
  <div class="wrap mh-grid">
    <div>
      <span class="mh-badge"><i aria-hidden="true"></i>Coming soon for mental health practices</span>
      <h1>Memberships for <em>mental health</em> practices.</h1>
      <p class="lead2">We are getting MemberCloud ready for therapy and counseling practices. Join the waitlist and we will let you know the day it opens.</p>
      <div class="hero-actions2"><a class="btn btn-dark" href="#demo">Join the waitlist <span aria-hidden="true">&rsaquo;</span></a><a class="tlink" href="#coming">What is coming</a></div>
    </div>
    <figure class="mh-media"><video src="{src}" poster="{poster}" autoplay muted loop playsinline preload="metadata" aria-label="{esc(alt)}"></video>
      <figcaption><span>{ic('mood-smile')}</span>Built with the same simple tools practices already use.</figcaption></figure>
  </div>
</section>

<section class="mh-sec tint lp-sec" id="coming" style="padding-block:clamp(64px,8vw,112px)">
  <div class="wrap">
    <h2 class="lp-h2">The same simple tools, set up for your practice.</h2>
    <div class="mh-cards">{cards}</div>
  </div>
</section>

<section class="mh-sec">
  <div class="wrap">
    <div class="mh-band"><img src="real/p-mental.jpg" alt="" width="1120" height="1500" loading="lazy"><div><h2>Opening with care.</h2><p>We are finalizing the details for this industry so it is ready when you are. Waitlist practices hear first.</p></div></div>
  </div>
</section>

<section class="mh-sec" style="padding-top:0">
  <div class="wrap">
    <h2 class="lp-h2">Three simple steps.</h2>
    <div class="mh-steps">{steps}</div>
    <div class="mh-more"><span>Explore other industries:</span>{others}</div>
  </div>
</section>

<section class="mh-sec" id="demo" style="padding-top:0">
  <div class="wrap">
    <div class="mh-wait">
      <div><h2>Join the waitlist.</h2><p>Tell us about your practice and we will email you when MemberCloud opens for mental health.</p><div class="contact"><span>(888) 408-7007</span><span>info@member-cloud.com</span></div></div>
      <div class="mh-form"><h3>Your details</h3>{form_html(p['form'], waitlist=True)}</div>
    </div>
  </div>
</section>

<section id="faq">
  <div class="wrap faq-grid">
    <h2>Questions owners ask first.</h2>
    <div>{faq_html}</div>
  </div>
</section>
"""


def page(p):
    soon = bool(p.get('soon'))
    steps = ''.join(f'<div class="step"><b>0{i + 1}</b><h3>{esc(t)}</h3><p>{esc(d.format(who=p["who"]))}</p></div>' for i, (t, d) in enumerate(STEPS_SOON if soon else STEPS))
    month = p['fee'] * p['members']
    be = math.ceil(149 / p['fee'])
    faq = [FAQ['alongside'][0].format(sw=p['sw']), FAQ['alongside'][1]], list(FAQ['custom']), list(FAQ['trial']), list(FAQ['where'])
    faq_items = [list(x) for x in faq] + [list(x) for x in p['extra_faq']]
    if soon: faq_items = [list(x) for x in p['extra_faq']] + [list(FAQ['alongside'][:1] and (FAQ['alongside'][0].format(sw=p['sw']), FAQ['alongside'][1])), list(FAQ['where'])]
    faq_html = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq_items)
    benefits = ''.join(f'<div class="bcard"><i>{ic(p["bicons"][i])}</i><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, (t, d) in enumerate(p['benefits']))
    others = ''.join(f'<a href="{o["file"]}">{esc(o["label"])}</a>' for o in PAGES if o['slug'] != p['slug'])
    opts = ''.join(f'<option value="{v}"{" selected" if v == p["form"] else ""}>{esc(l)}</option>' for v, l in TYPES)
    tag, price, planp = p['plan']
    tiers = ''.join(f'<button type="button" class="tier" data-fee="{pr_.strip("$")}" data-name="{esc(n)}" data-text="{esc(d)}" aria-pressed="{"true" if int(pr_.strip("$")) == p["fee"] else "false"}"><span class="ti">{ic(p["ticons"][i])}</span><span class="tn">{esc(n)}</span><b class="num">{esc(pr_)}<small>/ month</small></b><p>{esc(d)}</p><span class="pick">Try it in the calculator below</span></button>' for i, (n, pr_, d) in enumerate(p['tiers']))
    chips = ''
    if p.get('chips'):
        chips = '<div class="chips">' + ''.join(f'<span>{esc(c)}</span>' for c in p['chips']) + '</div><p class="chips-src">Source: Free Exercise DB, a public domain dataset (github.com/yuhonas/free-exercise-db).</p>'
    pr = p['proof']
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(p['title'])}</title>
<meta name="description" content="{esc(p['desc'])}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@200..700&display=swap">
<style>{BASE_CSS}{LP_CSS}{DD_CSS}{BCSS}{MH_CSS if soon else ""}</style></head><body>
<a class="skip" href="#main">Skip to content</a>
<div class="canvas">
<header class="topbar">
  <div class="wrap tb-in">
    <a class="brand" href="index.html" aria-label="MemberCloud home"><img src="images/logo-horizontal.png" alt="MemberCloud" width="1800" height="338"></a>
    <nav class="navlinks" aria-label="Primary">
      {dd_html(p["slug"])}
      <a href="#benefits">How it helps</a>
      {'' if soon else '<a href="#plans">Plan ideas</a>'}
      <a href="{'#demo' if soon else '#pricing'}">{'Waitlist' if soon else 'Pricing'}</a>
      <a href="#faq">FAQ</a>
    </nav>
    <a class="btn btn-dark tb-cta" href="#demo"><span class="long">Book a free demo</span><span class="short">Free demo</span></a>
  </div>
</header>
<main id="main">
<section class="lp-hero" id="top">
  <div class="wrap lp-grid">
    <div>
      <h1>{esc(p['h1'])}</h1>
      <p class="lead2">{esc(p['lead'])}</p>
      <div class="hero-actions2">
        <a class="btn btn-ring" href="#demo">{'Join the waitlist' if soon else 'Book a free demo'} <span aria-hidden="true">&rsaquo;</span></a>
        {'' if soon else '<a class="tlink" href="#pricing">See pricing</a>'}
      </div>
      <p class="lp-note">{'We will email you as soon as it opens.' if soon else '$149 a month. No hidden fees.'}</p>
    </div>
    {media_html(p)}
  </div>
</section>

<section class="lp-sec tint" id="benefits">
  <div class="wrap">
    <h2 class="lp-h2">{esc(p['h2'])}</h2>
    <p class="lp-sub">{esc(p['sub'])}</p>
    <div class="bgrid">{benefits}</div>
  </div>
</section>

{'' if soon else f'''<section class="lp-sec" id="plans">
  <div class="wrap">
    <h2 class="lp-h2">{esc(p['tiers_h'])}</h2>
    <p class="lp-sub">{esc(p['tiers_sub'])}</p>
    <div class="tiers">{tiers}</div>
    {chips}
    <p class="lp-note">Examples only. You choose your own names, prices and what each plan includes.</p>
  </div>
</section>

<section class="lp-sec tint" id="example">
  <div class="wrap">
    <h2 class="lp-h2">A plan your {esc(p['member_word'])} will understand.</h2>
    <div class="ex-grid">
      <div class="plan-card"><span class="tag" id="pc-tag">{esc(tag)}</span><b class="num" id="pc-price">{esc(price)}</b><p id="pc-text">{esc(planp)}</p></div>
      <div class="math-card" id="calc">
        <div class="calc">
          <label for="c-mem">{esc(p['member_word'].capitalize())} <output id="o-mem">{p['members']}</output></label>
          <input id="c-mem" type="range" min="10" max="300" step="5" value="{p['members']}">
          <label for="c-fee">Monthly price <output id="o-fee">${p['fee']}</output></label>
          <input id="c-fee" type="range" min="10" max="200" step="1" value="{p['fee']}">
        </div>
        <div class="row"><span>Per month</span><strong id="r-month">{money(month)}</strong></div>
        <div class="row"><span>Per year</span><strong id="r-year">{money(month * 12)}</strong></div>
        <div class="row"><span>{esc(p['member_word'].capitalize())} to cover the $149 fee</span><strong id="r-be">{be}</strong></div>
        <p class="fine">Example only. Move the sliders or pick a plan above. Your price and number of {esc(p['member_word'])} will differ.</p>
      </div>
    </div>
  </div>
</section>

'''}

{'' if soon else walkthrough_html(WT[p['slug']])}

{proof_html(p)}

{reviews_html() if p['slug'] == 'dental' else ''}

<section class="lp-sec tint">
  <div class="wrap">
    <h2 class="lp-h2">{'What happens next.' if soon else 'From demo to recurring revenue.'}</h2>
    <div class="steps">{steps}</div>
    <div class="others"><span style="align-self:center;color:var(--muted)">Other industries:</span>{others}<a href="index.html#guides">All industries</a></div>
  </div>
</section>

<section class="action" id="pricing">
  <img src="real/huddle.jpg" alt="" width="1800" height="1005" loading="lazy">
  <img class="wm" src="images/mark-white.png" alt="" width="600" height="500" loading="lazy">
  <div class="wrap">
    {'' if soon else f'''    <div class="price">
      <div>
        <h2>Pricing that doesn't punish you for growing.</h2>
        <div class="amt num" style="margin-top:40px">$149<small>/ month</small></div>
        <p class="cap">Everything you need to launch memberships today.</p>
        <p class="fine">Introductory pricing for a limited time.</p>
      </div>
      <ul>
        <li>Unlimited admins</li>
        <li>Unlimited locations</li>
        <li>Tiered memberships you can set up quickly</li>
        <li>Automated billing</li>
      </ul>
    </div>'''}
    <div class="cta" id="demo">
      <div>
        <h2>{'Join the waitlist for mental health practices.' if soon else 'Book a free demo for your ' + esc(p['who']) + '.'}</h2>
        <p class="lead">{'Tell us about your practice and we will email you when MemberCloud opens for mental health.' if soon else 'Increase loyalty and reclaim staff time with MemberCloud. We will show it with your own plans.'}</p>
        <div class="contact"><span>(888) 408-7007</span><span>info@member-cloud.com</span></div>
      </div>
      {form_html(p['form'], waitlist=soon)}
    </div>
  </div>
</section>

<section id="faq">
  <div class="wrap faq-grid">
    <h2>Questions owners ask first.</h2>
    <div>{faq_html}</div>
  </div>
</section>
<a class="btn btn-dark mcta" id="mcta" href="#demo">Book a free demo</a>
{contact_card_html()}
</main>

<footer>
  <div class="wrap foot">
    <div><a class="brand" href="index.html" aria-label="MemberCloud home"><img src="images/logo-horizontal.png" alt="MemberCloud" width="1800" height="338"></a><p class="foot-addr">900 SE Ocean Blvd, Suite B-118, Stuart, FL 34994</p></div>
    <nav class="foot-links" aria-label="Footer">
      <a href="privacy.html">Privacy Policy</a>
      <a href="https://membercloud.net">Log in</a>
      <a href="https://www.linkedin.com/company/member-cloud/">LinkedIn</a>
      <a href="https://www.instagram.com/member.cloud/">Instagram</a>
      <a href="https://www.facebook.com/profile.php?id=100092513314162">Facebook</a>
    </nav>
  </div>
</footer>
</div>
<script>
{DD_JS}
(function () {{
  function $(id) {{ return document.getElementById(id); }}
  var mem = $('c-mem'), fee = $('c-fee');
  function fmt(n) {{ return '$' + Math.round(n).toLocaleString('en-US'); }}
  function calc() {{
    var a = +mem.value, f = +fee.value;
    $('o-mem').textContent = a; $('o-fee').textContent = '$' + f;
    $('r-month').textContent = fmt(a * f); $('r-year').textContent = fmt(a * f * 12);
    $('r-be').textContent = Math.ceil(149 / f);
  }}
  if (mem && fee) {{ mem.addEventListener('input', calc); fee.addEventListener('input', calc); }}
  var tiers = document.querySelectorAll('button.tier');
  tiers.forEach(function (t) {{
    t.addEventListener('click', function () {{
      tiers.forEach(function (x) {{ x.setAttribute('aria-pressed', x === t ? 'true' : 'false'); }});
      fee.value = t.getAttribute('data-fee'); calc();
      $('pc-tag').textContent = t.getAttribute('data-name'); $('pc-price').textContent = '$' + fee.value + ' / month'; $('pc-text').textContent = t.getAttribute('data-text');
      $('calc').scrollIntoView({{ behavior: 'smooth', block: 'center' }});
    }});
  }});
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {{
    var rv = new IntersectionObserver(function (es) {{ es.forEach(function (e) {{ if (e.isIntersecting) {{ e.target.classList.add('in'); rv.unobserve(e.target); }} }}); }}, {{ threshold: 0.15 }});
    document.querySelectorAll('.bcard, .tier, .step, .plan-card, .math-card').forEach(function (el, i) {{ el.classList.add('rv'); el.style.transitionDelay = (i % 4) * 70 + 'ms'; rv.observe(el); }});
  }}
  if ('IntersectionObserver' in window) {{
    var m = $('mcta'), st = {{ hero: true, action: false }};
    function upd() {{ m.classList.toggle('show', !st.hero && !st.action); }}
    new IntersectionObserver(function (es) {{ st.hero = es[0].isIntersecting; upd(); }}).observe($('top'));
    new IntersectionObserver(function (es) {{ st.action = es[0].isIntersecting; upd(); }}, {{ threshold: 0.05 }}).observe(document.querySelector('.action') || document.querySelector('#demo') || document.querySelector('footer'));
  }}
}})();
</script>
<script>{BJS}</script>
<script src="chat/chat.js" defer></script>
</body></html>
"""
    if soon:
        a = doc.index('<main id="main">') + len('<main id="main">'); z = doc.index('<a class="btn btn-dark mcta"')
        doc = doc[:a] + soon_main(p, faq_html, others) + doc[z:]
    return doc


for p in PAGES:
    open(p['file'], 'w', encoding='utf-8').write(page(p))
    print('wrote', p['file'])


# ---------------------------------------------------------------- privacy policy (text as published on member-cloud.com/privacy-policy)
PRIVACY = [
    (None, ['Thank you for visiting the MemberCloud website. This Privacy Policy outlines how we collect, use, and protect the information you provide while using our website and services. By accessing our website or using our services, you consent to the practices described in this policy.']),
    ('Information We Collect', ['We may collect personal information such as names, email addresses, and phone numbers when you voluntarily submit it through our website\'s forms, during the sign-up process, or while using our services. We may also collect non-personal information, such as browser types, device information, and browsing patterns, to enhance user experience and improve our services.']),
    ('How We Use Your Information', ['We use the collected information for the following purposes:', ['To provide and improve our services', 'To personalize user experience', 'To communicate with you about our services, promotions, and updates', 'To process payments and invoices', 'To monitor website traffic and usage patterns', 'To comply with legal obligations']]),
    ('Data Security', ['We implement industry-standard security measures to protect the information we collect and store. However, please note that no method of data transmission over the internet or electronic storage is completely secure. We strive to protect your personal information, but we cannot guarantee its absolute security.']),
    ('Sharing of Information', ['We do not sell, trade, or otherwise transfer your personal information to third parties without your consent, except in cases where it\'s necessary to provide our services or as required by law.']),
    ('Cookies and Tracking', ['Our website may use cookies and similar tracking technologies to enhance your browsing experience and collect information about how you use our site. You can modify your browser settings to disable cookies, but this may affect the functionality of certain features on our website.']),
    ('Links to Third-Party Websites', ['Our website may contain links to third-party websites. We are not responsible for the content or privacy practices of these websites. We encourage you to review the privacy policies of these websites before providing any personal information.']),
    ('Changes to this Privacy Policy', ['We may update this Privacy Policy from time to time to reflect changes in our practices or legal requirements. The effective date at the top of the policy will indicate the most recent revisions. Your continued use of our website and services after any changes to this policy signify your acceptance of the changes.']),
    ('Contact Us', ['If you have any questions, concerns, or requests regarding this Privacy Policy, please contact us at <a href="mailto:info@member-cloud.com">info@member-cloud.com</a>.', '900 SE Ocean Blvd, Suite B-118, Stuart, FL 34994']),
]
PRIV_CSS = """
.legal { padding-block: clamp(48px, 7vw, 112px) clamp(80px, 10vw, 160px); }
.legal-grid { display: grid; grid-template-columns: 260px minmax(0, 1fr); gap: clamp(32px, 6vw, 96px); align-items: start; }
.legal h1 { font-size: clamp(40px, 5.4vw, 72px); font-weight: 500; letter-spacing: -0.045em; line-height: 1; color: var(--indigo); }
.legal .meta { margin-top: 18px; font-size: 15px; color: var(--muted); }
.legal .meta b { font-weight: 500; color: var(--ink); background: #FFF1D6; padding: 2px 8px; border-radius: 6px; }
.legal-toc { position: sticky; top: 110px; display: grid; gap: 4px; border-left: 1px solid var(--line); padding-left: 16px; }
.legal-toc a { font-size: 15px; color: var(--muted); text-decoration: none; padding: 6px 0; } .legal-toc a:hover { color: var(--indigo); }
.legal-body { max-width: 46em; }
.legal-body .intro { font-size: 21px; line-height: 1.55; color: var(--ink-2); }
.legal-body h2 { margin-top: 48px; font-size: clamp(24px, 2.4vw, 30px); font-weight: 500; letter-spacing: -0.03em; color: var(--indigo); scroll-margin-top: 110px; }
.legal-body p { margin-top: 14px; font-size: 18px; line-height: 1.65; color: var(--ink-2); }
.legal-body ul { margin: 14px 0 0; padding-left: 22px; display: grid; gap: 8px; font-size: 18px; line-height: 1.55; color: var(--ink-2); }
.legal-body a { color: var(--indigo); }
@media (max-width: 860px) { .legal-grid { grid-template-columns: 1fr; } .legal-toc { position: static; } }
"""


def privacy_page():
    import re as _re
    toc, body = '', ''
    for title, parts in PRIVACY:
        sid = _re.sub(r'[^a-z]+', '-', title.lower()).strip('-') if title else ''
        if title:
            toc += f'<a href="#{sid}">{title}</a>'
            body += f'<h2 id="{sid}">{title}</h2>'
        for x in parts:
            body += ('<ul>' + ''.join(f'<li>{i}</li>' for i in x) + '</ul>') if isinstance(x, list) else (f'<p class="intro">{x}</p>' if not title else f'<p>{x}</p>')
    doc = page(PAGES[0])
    a = doc.index('<main id="main">') + len('<main id="main">'); z = doc.index('<a class="btn btn-dark mcta"')
    main = f"""
<section class="legal" id="top">
  <div class="wrap legal-grid">
    <div><h1>Privacy Policy</h1><p class="meta">Effective date: <b>to be confirmed</b></p><nav class="legal-toc" aria-label="On this page" style="margin-top:32px">{toc}</nav></div>
    <div class="legal-body">{body}</div>
  </div>
</section>
"""
    doc = doc[:a] + main + doc[z:]
    doc = _re.sub(r'<title>.*?</title>', '<title>Privacy Policy | MemberCloud</title>', doc, count=1)
    doc = _re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="How MemberCloud collects, uses and protects the information you share on our website and services.">', doc, count=1)
    doc = doc.replace('</style>', PRIV_CSS + '</style>', 1)
    doc = doc.replace('<a href="#benefits">How it helps</a>', '').replace('<a href="#plans">Plan ideas</a>', '').replace('<a href="#pricing">Pricing</a>', '<a href="index.html#pricing">Pricing</a>').replace('<a href="#faq">FAQ</a>', '<a href="index.html#faq">FAQ</a>')
    doc = doc.replace('href="#demo"', 'href="index.html#demo"')
    return doc


open('privacy.html', 'w', encoding='utf-8').write(privacy_page())
print('wrote privacy.html')
