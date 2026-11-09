"""HTML replicas of the MemberCloud product screens (dashboard, people list, member detail, payments, public landing page, fees).
Menus and screen structure follow the real product screenshots. Each industry gets its own vocabulary and invented sample data."""
import html
from dd import ic

esc = html.escape
W, H = 1200, 640  # design size; the page scales it to fit

IND = {
    'dental': dict(
        people='Patients', person='Patient', page_label='Patient page', org='Demo Dental Studio', ini='DS',
        plans=[('Monthly Plan', 2), ('Tot Plan 0-2 years', 0), ('Yearly Plan', 3)], current=11, pastdue=6,
        rows=[('1042', 'Rivera Alex', 'Yearly Plan', 'December 16, 2026'), ('1043', 'Patel Jordan', 'Monthly Plan', 'November 16, 2026'), ('1044', 'Torres Sam', 'Yearly Plan', 'December 05, 2026')],
        failed=[('1051', 'Morgan Riley', 'Monthly Plan'), ('1052', 'Lee Casey', 'Monthly Plan'), ('1053', 'Kim Taylor', 'Monthly Plan')],
        member=dict(name='Alex Rivera', plan='Monthly Plan', price='$40.00 / Month', extra=None),
        details=[('D0120', 'Periodic exam', 2, 1), ('D0140', 'Limited exam, problem focused', 2, 0), ('D0220', 'X-ray, first image', 2, 1), ('D0230', 'X-ray, each additional image', 2, 0)],
        pay=[('Alex Rivera', 'Subscription Cycle', '$40.00'), ('Sam Torres', 'Subscription Create', '$40.00'), ('Sam Torres', 'Downpayment', '$35.00'), ('Jordan Patel', 'Subscription Cycle', '$40.00'), ('Alex Rivera', 'Subscription Create', '$40.00')],
        fees_title='UCR Fees', fees_form='UCR&rsquo;s Data', code_label='ADA Code', code_ph='Type the ADA code', fee_label='UCR Fee', fee_ph='Type the UCR fee', add='Add UCR fee', fees_card='UCR Fees',
        fees=[('D0120', 'Periodic exam', '$88.00 USD'), ('D0140', 'Limited exam, problem focused', '$96.00 USD'), ('D0150', 'Comprehensive exam', '$91.00 USD'), ('D0220', 'X-ray, first image', '$38.00 USD'), ('D0230', 'X-ray, each additional image', '$31.00 USD')],
        lp=dict(hero='No dental insurance? Here&rsquo;s an affordable alternative.', save='Save money on dental care', save_s='Get instant access to exceptional dentistry.', why_s='Discover how our dental membership plan differs.',
                why=[('No fine print', 'No waiting periods, copays, deductibles or annual maximums.', 'clipboard-check'), ('Essential care', 'Preventive care is included: exams, cleanings, fluoride and routine X-rays.', 'dental'), ('Transparent', 'Benefits and pricing are easy to understand and clearly outlined.', 'coin'), ('Instant access', 'Your benefits start the day you enroll.', 'hand-click')],
                plans_t='Preventive care plans at Demo Dental Studio',
                plans=[('Yearly Plan', '$389.98', '/Year', 'Ages: 3+', ['Professional cleanings (2 per year)', 'Doctor exams (2 per year)', 'Fluoride treatment', 'Necessary X-rays', 'One emergency exam per year', '20% off all other treatments'], 'heart'),
                       ('Tot Plan 0-2 Years', '$250', '/Year', 'Savings: $489', ['Doctor exam (2 per year)', 'Professional cleaning (2 per year)', 'Necessary X-rays', 'Fluoride treatment', 'One emergency exam per year', '10% off all other treatments'], 'mood-kid'),
                       ('Monthly Plan', '$40', '/Month', 'Savings: $602', ['Professional cleanings (2 per year)', 'Doctor exams (2 per year)', 'Fluoride treatment', 'Necessary X-rays', 'One emergency exam per year', '20% off all other treatments'], 'heart')])),
    'veterinary': dict(
        people='Clients', person='Client', page_label='Client page', org='Demo Animal Clinic', ini='AC',
        plans=[('Puppy and Kitten', 3), ('Adult Wellness', 5), ('Senior Care', 2)], current=10, pastdue=2,
        rows=[('2041', 'Rivera Alex (Max, Luna)', 'Adult Wellness', 'December 16, 2026'), ('2042', 'Patel Jordan (Bella)', 'Puppy and Kitten', 'November 16, 2026'), ('2043', 'Torres Sam (Rocky)', 'Senior Care', 'December 05, 2026')],
        failed=[('2051', 'Morgan Riley (Coco)', 'Adult Wellness'), ('2052', 'Lee Casey (Milo)', 'Puppy and Kitten'), ('2053', 'Kim Taylor (Daisy)', 'Adult Wellness')],
        member=dict(name='Alex Rivera', plan='Adult Wellness', price='$34.00 / Month', extra=('Pets:', 'Max (dog), Luna (cat)')),
        details=[('EXAM', 'Wellness exam', 2, 1), ('DHPP', 'DHPP vaccine', 1, 1), ('RAB', 'Rabies vaccine', 1, 0), ('FEC', 'Fecal test', 1, 0)],
        pay=[('Alex Rivera', 'Subscription Cycle', '$34.00'), ('Sam Torres', 'Subscription Create', '$44.00'), ('Jordan Patel', 'Subscription Cycle', '$29.00'), ('Riley Morgan', 'Subscription Cycle', '$34.00'), ('Alex Rivera', 'Subscription Create', '$34.00')],
        fees_title='Service Fees', fees_form='Service data', code_label='Service code', code_ph='Type the service code', fee_label='Fee', fee_ph='Type the fee', add='Add fee', fees_card='Service Fees',
        fees=[('EXAM', 'Wellness exam', '$65.00 USD'), ('DHPP', 'DHPP vaccine', '$38.00 USD'), ('RAB', 'Rabies vaccine', '$28.00 USD'), ('FEC', 'Fecal test', '$42.00 USD'), ('HWT', 'Heartworm test', '$45.00 USD')],
        lp=dict(hero='Keep every pet healthy for one monthly price.', save='Wellness care, made simple', save_s='Exams and vaccines for every pet in your household.', why_s='Discover how our pet wellness plans work.',
                why=[('One account', 'Every pet in the household under one plan and one payment.', 'paw'), ('Wellness included', 'Exams and core vaccines are part of the plan.', 'stethoscope'), ('Transparent', 'Benefits and pricing are easy to understand and clearly outlined.', 'coin'), ('Instant access', 'Your benefits start the day you enroll.', 'hand-click')],
                plans_t='Pet wellness plans at Demo Animal Clinic',
                plans=[('Puppy and Kitten', '$29', '/Month', 'First year of life', ['Wellness exams', 'First-year vaccine series', 'Deworming', 'Nail trims', '10% off other services'], 'bone'),
                       ('Adult Wellness', '$34', '/Month', 'Ages 1 to 7', ['Annual wellness exam', 'Core vaccines', 'Fecal and heartworm tests', 'Nail trims', '10% off other services'], 'dog'),
                       ('Senior Care', '$44', '/Month', 'Ages 8+', ['Two exams a year', 'Annual bloodwork', 'Core vaccines', 'Heartworm test', '15% off diagnostics'], 'heart')])),
    'gym': dict(
        people='Members', person='Member', page_label='Member page', org='Demo Studio', ini='DS',
        plans=[('Strength Floor', 14), ('Studio Unlimited', 22), ('Mobility and Recovery', 8)], current=44, pastdue=3,
        rows=[('3041', 'Rivera Alex', 'Studio Unlimited', 'December 16, 2026'), ('3042', 'Patel Jordan', 'Strength Floor', 'November 16, 2026'), ('3043', 'Torres Sam', 'Mobility and Recovery', 'December 05, 2026')],
        failed=[('3051', 'Morgan Riley', 'Studio Unlimited'), ('3052', 'Lee Casey', 'Strength Floor'), ('3053', 'Kim Taylor', 'Studio Unlimited')],
        member=dict(name='Alex Rivera', plan='Studio Unlimited', price='$89.00 / Month', extra=None),
        details=[('CLASS', 'Group classes', 'Unlimited', 12), ('GUEST', 'Guest pass', 1, 0), ('WKSP', 'Workshop, member price', 2, 1), ('RECOV', 'Recovery session', 1, 0)],
        pay=[('Alex Rivera', 'Subscription Cycle', '$89.00'), ('Sam Torres', 'Subscription Create', '$59.00'), ('Jordan Patel', 'Subscription Cycle', '$49.00'), ('Riley Morgan', 'Subscription Cycle', '$89.00'), ('Alex Rivera', 'Subscription Create', '$89.00')],
        fees_title='Services and add-ons', fees_form='Service data', code_label='Code', code_ph='Type the code', fee_label='Price', fee_ph='Type the price', add='Add service', fees_card='Services and add-ons',
        fees=[('PT60', 'Personal training, 60 min', '$75.00 USD'), ('GUEST', 'Guest pass', '$20.00 USD'), ('WKSP', 'Workshop', '$35.00 USD'), ('RECOV', 'Recovery session', '$40.00 USD'), ('TOWEL', 'Towel service', '$5.00 USD')],
        lp=dict(hero='Train more, pay less. Memberships at Demo Studio.', save='Pick the membership that fits', save_s='Classes, open floor and recovery in clear tiers.', why_s='Discover how our memberships work.',
                why=[('Clear tiers', 'Choose classes, open floor or recovery. Change any time.', 'list-check'), ('Classes included', 'Book the classes your plan includes.', 'yoga'), ('Transparent', 'Benefits and pricing are easy to understand and clearly outlined.', 'coin'), ('Instant access', 'Your membership starts the day you enroll.', 'hand-click')],
                plans_t='Memberships at Demo Studio',
                plans=[('Strength Floor', '$49', '/Month', 'Open floor access', ['Open access to the weight floor', 'Member pricing on workshops', 'One guest pass a quarter'], 'barbell'),
                       ('Studio Unlimited', '$89', '/Month', 'Most popular', ['Unlimited group classes', 'Open floor access', 'One guest pass a month', 'Member pricing on workshops'], 'yoga'),
                       ('Mobility and Recovery', '$59', '/Month', 'Stretch and recover', ['Stretching and mobility classes', 'Foam roll and bands area', 'One recovery session a month'], 'stretching')])),
    'any': dict(
        people='Members', person='Member', page_label='Member page', org='Demo Club', ini='DC',
        plans=[('Basic', 18), ('Plus', 12), ('Family', 6)], current=36, pastdue=2,
        rows=[('4041', 'Rivera Alex', 'Plus', 'December 16, 2026'), ('4042', 'Patel Jordan', 'Basic', 'November 16, 2026'), ('4043', 'Torres Sam', 'Family', 'December 05, 2026')],
        failed=[('4051', 'Morgan Riley', 'Plus'), ('4052', 'Lee Casey', 'Basic'), ('4053', 'Kim Taylor', 'Family')],
        member=dict(name='Alex Rivera', plan='Plus', price='$60.00 / Month', extra=None),
        details=[('VISIT', 'Monthly visit', 2, 1), ('GUEST', 'Guest pass', 1, 0), ('ADDON', 'Add-on service, member price', 2, 1), ('EVENT', 'Member event', 1, 0)],
        pay=[('Alex Rivera', 'Subscription Cycle', '$60.00'), ('Sam Torres', 'Subscription Create', '$90.00'), ('Jordan Patel', 'Subscription Cycle', '$30.00'), ('Riley Morgan', 'Subscription Cycle', '$60.00'), ('Alex Rivera', 'Subscription Create', '$60.00')],
        fees_title='Services', fees_form='Service data', code_label='Code', code_ph='Type the code', fee_label='Price', fee_ph='Type the price', add='Add service', fees_card='Services',
        fees=[('VISIT', 'Single visit', '$25.00 USD'), ('GUEST', 'Guest pass', '$15.00 USD'), ('ADDON', 'Add-on service', '$30.00 USD'), ('EVENT', 'Member event', '$20.00 USD'), ('RENT', 'Equipment rental', '$10.00 USD')],
        lp=dict(hero='Join the club. Memberships at Demo Club.', save='Membership, made simple', save_s='Pick a plan and enjoy member benefits from day one.', why_s='Discover how our memberships work.',
                why=[('Simple plans', 'Three clear options, billed monthly.', 'list-check'), ('Member benefits', 'Visits, guest passes and member pricing.', 'heart'), ('Transparent', 'Benefits and pricing are easy to understand and clearly outlined.', 'coin'), ('Instant access', 'Your membership starts the day you enroll.', 'hand-click')],
                plans_t='Memberships at Demo Club',
                plans=[('Basic', '$30', '/Month', 'The essentials', ['Two visits a month', 'Member pricing on services'], 'user'),
                       ('Plus', '$60', '/Month', 'Most popular', ['Unlimited visits', 'One guest pass a month', 'Member pricing on services'], 'users'),
                       ('Family', '$90', '/Month', 'For the household', ['Plus benefits for the household', 'Two guest passes a month', 'Member events'], 'users-group')])),
}


def nav(active, c):
    items = [('Dashboard', 'home', False), ('Landing Page', 'device-laptop', True), ('Plans', 'receipt-dollar', True), ('Team Members', 'user-check', True),
             (c['people'], 'users-group', True), ('Appointments', 'calendar-check', True), ('Payments', 'cash', True), ('Marketing', 'mail-check', True)]
    return ''.join(f'<span class="rp-ni{" on" if n == active else ""}">{ic(i)}<b>{n}</b>{ic("chevron-down") if ch else ""}</span>' for n, i, ch in items)


def top():
    return f'<div class="rp-top"><img src="images/logo-horizontal.png" alt="" width="1800" height="338"><span class="rp-user"><i>DM</i>Demo MemberCloud {ic("chevron-down")}</span></div>'


def shell(c, active, title, body, sub='Membership Demo'):
    return (f'{top()}<div class="rp-main"><nav class="rp-nav" aria-hidden="true">{nav(active, c)}</nav>'
            f'<div class="rp-content"><div class="rp-ban"><span>{esc(sub)}</span><h5>{esc(title)}</h5></div><div class="rp-av">{c["ini"]}</div>{body}</div></div>')


def card(title, inner, extra=''):
    return f'<div class="rp-card {extra}"><div class="rp-ch">{ic("list-check")}<b>{esc(title)}</b></div>{inner}</div>'


def toolbar():
    return '<div class="rp-tb"><span>Show <i class="rp-sel">5</i> entries</span><span>Search: <i class="rp-in"></i></span><span class="rp-btns"><u class="g">Excel</u><u class="o">PDF</u><u class="b">CSV</u><u class="g">Print</u><u class="g">Column visibility &#9662;</u></span></div>'


def table(head, rows, foot):
    th = ''.join(f'<th>{esc(x)}</th>' for x in head)
    tr = ''.join('<tr>' + ''.join(f'<td data-l="{esc(head[i])}">{cell}</td>' for i, cell in enumerate(r)) + '</tr>' for r in rows)
    return f'{toolbar()}<table class="rp-t cardify"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table><div class="rp-ft"><span>{esc(foot)}</span><span class="rp-pg"><i>Previous</i><i class="on">1</i><i>Next</i></span></div>'


ACT = f'<span class="rp-act">{ic("user-edit")}{ic("file-invoice")}{ic("cash")}{ic("mail")}</span>'
chip = lambda t, k: f'<span class="rp-st st-{k}">{t}</span>'


def dashboard(c):
    mx = max(4, max(n for _, n in c['plans']))
    top_ = (mx + 3) // 4 * 4
    ys = ''.join(f'<i>{top_ - k * top_ // 4}</i>' for k in range(5))
    cols = ''.join(f'<div class="rp-col"><div class="rp-bar" data-h="{round(n / top_ * 100)}"></div><span>{esc(p)}</span></div>' for p, n in c['plans'])
    chart = f'<div class="rp-chart"><div class="rp-y">{ys}</div><div class="rp-plot">{cols}</div></div>'
    tbl = '<table class="rp-t sm"><thead><tr><th>Plan</th><th>Amount</th></tr></thead><tbody>' + ''.join(f'<tr><td>{esc(p)}</td><td class="c">{n}</td></tr>' for p, n in c['plans']) + '</tbody></table>'
    left = card('Current Active Members by Plan', f'<div class="rp-chartrow">{chart}{tbl}</div>', 'rp-w')
    right = (f'<div class="rp-stats"><div class="rp-stat"><b class="rp-num" data-to="{c["current"]}">{c["current"]}</b><span>Current Members</span></div>'
             f'<div class="rp-stat"><b class="rp-num" data-to="{c["pastdue"]}">{c["pastdue"]}</b><span>Current Members Past Due</span></div></div>')
    added = card('Members Added By', '<div class="rp-fr" style="padding:14px 16px;grid-template-columns:1fr 1fr auto"><div><label>Start Date</label><i class="v">10/01/2026</i></div><div><label>End Date</label><i class="v">10/24/2026</i></div></div>', 'rp-added')
    return shell(c, 'Dashboard', 'Dashboard', f'<div class="rp-row">{left}{right}</div>{added}')


def people(c):
    top_ = f'<div class="rp-acts"><span class="rp-nb">+ Add {c["person"]}</span><span class="rp-nb">Upload File</span></div>'
    t1 = card(f'Active {c["people"].lower()} with credit card payment', table([f'{c["person"]} Id', 'Name', 'Plan', 'Payment Method', 'Next Invoice', 'Status', 'Action'],
              [[i, n, p, 'Card', d, chip('Active', 'g' if k else 'o'), ACT] for k, (i, n, p, d) in enumerate(c['rows'])], f'Showing 1 to 3 of 3 entries'))
    t2 = card('Failed Payments', table([f'{c["person"]} Id', 'Name', 'Plan', 'Payment Method', 'Status', 'Action'],
              [[i, n, p, 'Card', chip('Failed Payment', 'a'), ACT] for i, n, p in c['failed']], 'Showing 1 to 3 of 3 entries'))
    return shell(c, c['people'], c['people'], top_ + t1 + t2)


def member(c):
    m = c['member']
    kv = [('Billed by:', c['org']), ('Responsible Party:', m['name'])] + ([m['extra']] if m['extra'] else []) + [('Current plan:', m['plan']), ('Price:', m['price']), ('Method of payment:', 'Visa ending in 4242'),
          ('Membership status:', 'Active'), ('Contract:', f'<span class="rp-link">{ic("file-type-pdf")}View Contract</span>'), ('Member since:', 'October 16, 2026'), ('Plan expiration date:', 'October 16, 2027')]
    rows = ''.join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in kv)
    plan = ('<table class="rp-t sm cardify"><thead><tr><th>Code</th><th>Description</th><th>Available Amount</th><th>Amount Used</th><th>Action</th></tr></thead><tbody>'
            + ''.join(f'<tr><td data-l="Code">{a}</td><td data-l="Description">{b}</td><td class="c" data-l="Available">{x}</td><td class="c" data-l="Used">{y}</td><td class="c" data-l="Action">{ic("pencil")}</td></tr>' for a, b, x, y in c['details']) + '</tbody></table>')
    modal = (f'<div class="rp-modal"><span class="rp-x">&times;</span><h6>{m["name"]}</h6>'
             f'<div class="rp-card"><div class="rp-ch">{ic("list-check")}<b>Membership</b></div><table class="rp-kv">{rows}</table></div>'
             f'<div class="rp-card"><div class="rp-ch">{ic("list-check")}<b>Plan Details</b></div>{plan}</div></div>')
    base = shell(c, c['people'], c['people'], f'<div class="rp-acts"><span class="rp-nb">+ Add {c["person"]}</span><span class="rp-nb">Upload File</span></div>')
    return f'{base}<div class="rp-dim"></div>{modal}'


def payments(c):
    dates = ['10/16/2026, 11:21 AM', '10/08/2026, 08:36 AM', '10/08/2026, 08:36 AM', '09/16/2026, 01:02 PM', '09/16/2026, 10:20 AM']
    inv = ['CAC00E71-0002', '51BE198C-0001', 'pi_3Qez...6g', '658BF642-0003', 'CAC00E71-0001']
    per = ['Oct 16 to Nov 16', 'Oct 8 to Nov 8', 'Oct 8 to Oct 8', 'Sep 16 to Oct 16', 'Sep 16 to Oct 16']
    rows = [[dates[i], n, inv[i], d, per[i], a, ic('receipt-dollar')] for i, (n, d, a) in enumerate(c['pay'])]
    body = card('Payments', table(['Created at', f'{c["person"]} Name', 'Invoice', 'Description', 'Period', 'Amount', 'Action'], rows, 'Showing 1 to 5 of 64 entries'))
    return shell(c, 'Payments', 'Payments', body)


def fees(c):
    tr = ''.join(f'<tr><td data-l="Code">{a}</td><td data-l="Description">{b}</td><td class="c" data-l="{c["fee_label"]}">{x}</td><td class="c" data-l="Updated">10/02/2026, 07:2{i} a.m.</td><td class="c" data-l="Action">{ic("pencil")}{ic("trash")}</td></tr>' for i, (a, b, x) in enumerate(c['fees']))
    form = (f'<div class="rp-form"><h6>{c["fees_form"]}</h6><div class="rp-fr" data-add="{c["add"]}"><div><label>{c["code_label"]}</label><i>{c["code_ph"]}</i></div><div><label>Currency</label><i class="v">USD</i></div><div><label>{c["fee_label"]}</label><i>{c["fee_ph"]}</i></div></div></div>')
    tbl = f'<div class="rp-card"><div class="rp-ch">{ic("list-check")}<b>{c["fees_card"]}</b></div>{toolbar()}<table class="rp-t cardify"><thead><tr><th>Code</th><th>Description</th><th>{c["fee_label"]}</th><th>Updated</th><th></th></tr></thead><tbody>{tr}</tbody></table></div>'
    body = f'<div class="rp-plain"><h4>{c["fees_title"]}</h4>{form}{tbl}<h4 class="mt">Membership Plan Fee Schedules</h4></div>'
    return f'{top()}<div class="rp-main"><nav class="rp-nav" aria-hidden="true">{nav("Plans", c)}</nav><div class="rp-content">{body}</div></div>'


def landing(c):
    lp = c['lp']
    tiles = ''.join(f'<div class="pp-tile {"t-a" if i % 2 == 0 else "t-b"}">{ic(icn)}<h6>{t}</h6><p>{d}</p></div>' for i, (t, d, icn) in enumerate(lp['why']))
    pc = ''.join(f'<div class="pp-plan{" on" if i == 1 else ""}">{ic(icn)}<h6>{n}</h6><div class="pr"><em>{p}</em><small>{u}</small></div><p class="sv">{s}</p><ul>' + ''.join(f'<li>{x}</li>' for x in li) + '</ul><span class="pp-btn">Enroll</span></div>'
                 for i, (n, p, u, s, li, icn) in enumerate(lp['plans']))
    return f"""<div class="pp-page"><div class="pp-bar" data-org="{esc(c['org'])}"><span class="rp-nb">Login</span></div>
<div class="pp-hero"><h5>Membership Demo</h5><p>{lp['hero']}</p><div><span class="pp-pill">Choose a Plan</span><span class="pp-pill">Learn More</span></div></div>
<h4 class="pp-h">{lp['save']}</h4><p class="pp-s">{lp['save_s']}</p>
<h4 class="pp-h">Why join?</h4><p class="pp-s">{lp['why_s']}</p><div class="pp-tiles">{tiles}</div>
<div class="pp-hero sm"><h5>Which plan is best for you?</h5><p>{lp['plans_t']}</p></div><div class="pp-plans">{pc}</div></div>"""


PANELS = [('dashboard', dashboard), ('patients', people), ('member', member), ('payments', payments), ('landing', landing), ('fees', fees)]


def panels_html(ind='dental'):
    c = IND[ind]
    return ''.join(f'<div class="rp-panel{" pp" if k == "landing" else ""}" data-k="{k}" hidden>{fn(c)}</div>' for k, fn in PANELS)


CSS = """
/* product screen replicas, restyled to the site (design size 1200 x 640, scaled to fit). Menus and items follow the real product. */
.rp-wrap { background: #fff; border-radius: 24px; overflow: hidden; box-shadow: 0 50px 100px -40px rgba(0,0,0,.75), 0 0 0 1px rgba(255,255,255,.08); position: relative; }
.rp-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.rp { width: 1200px; height: 640px; transform-origin: 0 0; -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; position: relative; background: #F3F6FB; color: #0A1A40; font-family: 'Outfit', system-ui, sans-serif; font-size: 14px; overflow: hidden; }
.rp-panel { position: absolute; inset: 0; } .rp-panel[hidden] { display: none; }
.rp-panel.pp { overflow-y: auto; background: #fff; }
.rp-top { height: 60px; background: #fff; display: flex; align-items: center; justify-content: space-between; padding: 0 22px; border-bottom: 1px solid #DCE3EF; }
.rp-top img { height: 28px; width: auto; }
.rp-user { font-size: 14px; color: #556182; display: flex; gap: 8px; align-items: center; } .rp-user i { font-style: normal; width: 32px; height: 32px; border-radius: 50%; background: #002466; color: #87C728; display: grid; place-items: center; font-size: 12px; font-weight: 600; } .rp-user svg { width: 14px; height: 14px; }
.rp-main { display: grid; grid-template-columns: 210px 1fr; height: calc(100% - 60px); }
.rp-nav { background: #00184A; padding: 16px 12px; display: grid; align-content: start; gap: 4px; }
.rp-ni { display: flex; align-items: center; gap: 11px; padding: 10px 12px; color: rgba(255,255,255,.78); font-size: 14px; border-radius: 12px; }
.rp-ni svg { width: 20px; height: 20px; color: #87C728; flex: none; } .rp-ni b { font-weight: 400; flex: 1; } .rp-ni svg:last-child:not(:first-child) { width: 13px; height: 13px; color: rgba(255,255,255,.5); }
.rp-ni.on { background: #87C728; color: #00184A; } .rp-ni.on b { font-weight: 600; } .rp-ni.on svg { color: #00184A !important; }
.rp-content { overflow: hidden; position: relative; padding: 16px 20px 0; }
.rp-ban { height: 112px; border-radius: 18px; background: radial-gradient(circle at 88% 20%, rgba(135,199,40,.45), transparent 32%), linear-gradient(110deg, #002466 0%, #00184A 100%); position: relative; overflow: hidden; color: #fff; display: grid; align-content: center; padding-left: 128px; gap: 2px; }
.rp-ban span { font-size: 12px; letter-spacing: .1em; text-transform: uppercase; color: #87C728; font-weight: 500; } .rp-ban h5 { margin: 0; font-size: 30px; font-weight: 500; letter-spacing: -0.03em; }
.rp-av { position: absolute; left: 44px; top: 34px; width: 72px; height: 72px; border-radius: 18px; background: #fff; color: #002466; z-index: 2; display: grid; place-items: center; font-weight: 600; font-size: 20px; box-shadow: 0 10px 24px -10px rgba(0,24,74,.6); }
.rp-row { display: grid; grid-template-columns: 1fr 200px; gap: 14px; margin-top: 14px; }
.rp-card { background: #fff; border: 1px solid #DCE3EF; border-radius: 16px; margin: 12px 0; overflow: hidden; }
.rp-row .rp-card { margin: 0; }
.rp-ch { display: flex; align-items: center; gap: 9px; padding: 12px 16px; border-bottom: 1px solid #EDF1F7; color: #002466; font-size: 15px; } .rp-ch b { font-weight: 500; } .rp-ch svg { width: 18px; height: 18px; color: #4B8010; padding: 5px; box-sizing: content-box; background: #EEF7DC; border-radius: 8px; }
.rp-chartrow { display: grid; grid-template-columns: 1.25fr 1fr; gap: 18px; padding: 16px; }
.rp-chart { display: grid; grid-template-columns: 22px 1fr; height: 230px; } .rp-y { display: flex; flex-direction: column; justify-content: space-between; font-size: 12px; color: #556182; padding-bottom: 24px; text-align: right; padding-right: 8px; }
.rp-plot { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; padding: 0 10px; border-bottom: 1px solid #DCE3EF; background: repeating-linear-gradient(#fff 0 51px, #EDF1F7 51px 52px); }
.rp-col { display: flex; flex-direction: column; justify-content: flex-end; align-items: center; position: relative; } .rp-col span { position: absolute; bottom: -22px; font-size: 12px; color: #556182; white-space: nowrap; }
.rp-bar { width: 70%; border-radius: 10px 10px 0 0; background: linear-gradient(#87C728, #4B8010); height: 0; transition: height .9s cubic-bezier(.16,1,.3,1); }
.rp-stats { display: grid; gap: 14px; } .rp-stat { background: #fff; border: 1px solid #DCE3EF; border-radius: 16px; padding: 16px; display: grid; gap: 6px; align-content: center; min-height: 128px; } .rp-stat b { font-size: 52px; line-height: 1; font-weight: 300; letter-spacing: -0.05em; } .rp-stat span { font-size: 14px; color: #556182; line-height: 1.2; }
.rp-stat:first-child b { color: #002466 !important; } .rp-stat:last-child b { color: #4B8010 !important; }
.rp-t { width: 100%; border-collapse: collapse; font-size: 13px; } .rp-t th { text-align: left; font-weight: 500; padding: 9px 12px; color: #556182; font-size: 11.5px; letter-spacing: .06em; text-transform: uppercase; white-space: nowrap; background: #F7F9FC; } .rp-t td { padding: 9px 12px; white-space: nowrap; border-top: 1px solid #EDF1F7; background: #fff; } .rp-t .c { text-align: center; } .rp-t svg { display: inline-block; width: 17px; height: 17px; vertical-align: middle; margin: 0 4px; color: #556182; }
.rp-t.sm { border: 1px solid #EDF1F7; border-radius: 12px; overflow: hidden; height: fit-content; }
.rp-tb { display: flex; justify-content: space-between; align-items: center; padding: 10px 16px; font-size: 13px; gap: 10px; color: #556182; }
.rp-sel, .rp-in { display: inline-block; font-style: normal; border: 1px solid #DCE3EF; border-radius: 999px; padding: 4px 22px 4px 12px; min-width: 52px; color: #0A1A40; } .rp-in { min-width: 140px; height: 28px; vertical-align: middle; }
.rp-btns { display: flex; gap: 6px; } .rp-btns u { text-decoration: none; padding: 6px 12px; border: 1px solid #DCE3EF; border-radius: 999px; font-weight: 500; background: #fff; color: #002466; } .rp-btns .g:first-child { color: #4B8010; } .rp-btns .o { color: #C2410C; } .rp-btns .b { color: #1D4ED8; }
.rp-ft { display: flex; justify-content: space-between; align-items: center; padding: 10px 16px; color: #556182; font-size: 13px; } .rp-pg { display: flex; gap: 4px; } .rp-pg i { font-style: normal; border-radius: 999px; padding: 5px 12px; color: #556182; } .rp-pg i.on { background: #002466; color: #fff; }
.rp-st { display: inline-block; padding: 4px 12px; border-radius: 999px; font-weight: 500; font-size: 12.5px; } .rp-st.st-o { background: #FFF1D6; color: #8A5A00; } .rp-st.st-g { background: #EEF7DC; color: #3F6E0C; } .rp-st.st-a { background: #FDE7D3; color: #B4420C; } .rp-st.st-r { background: #FDE8E8; color: #B42318; }
.rp-act { display: inline-flex; gap: 10px; } .rp-act svg { display: inline-block; width: 18px; height: 18px; margin: 0; color: #002466; }
.rp-acts { display: flex; justify-content: flex-end; gap: 8px; margin-top: -48px; padding-right: 16px; position: relative; z-index: 3; }
.rp-nb { display: inline-block; background: #87C728; color: #00184A; padding: 10px 18px; border-radius: 999px; font-weight: 600; font-size: 13.5px; } .rp-acts .rp-nb + .rp-nb { background: #fff; }
.rp-dim { position: absolute; inset: 60px 0 0 0; background: rgba(0,24,74,.5); backdrop-filter: blur(2px); z-index: 5; }
.rp-modal { position: absolute; z-index: 6; left: 250px; top: 24px; width: 700px; background: #fff; border-radius: 22px; padding: 18px 24px 0; height: 640px; overflow: hidden; box-shadow: 0 30px 80px rgba(0,24,74,.45); }
.rp-modal h6 { margin: 0 0 6px; font-size: 28px; text-align: left; color: #002466; font-weight: 500; letter-spacing: -0.03em; } .rp-modal .rp-card { margin: 10px 0; } .rp-x { position: absolute; right: 22px; top: 14px; font-size: 26px; color: #556182; }
.rp-kv { width: 100%; border-collapse: collapse; font-size: 13.5px; } .rp-kv th { width: 45%; text-align: left; padding: 8px 16px; font-weight: 400; color: #556182; border-top: 1px solid #EDF1F7; } .rp-kv td { padding: 8px 16px; font-weight: 500; border-top: 1px solid #EDF1F7; } .rp-link { display: inline-flex; align-items: center; gap: 4px; color: #002466; text-decoration: underline; } .rp-link svg { width: 17px; height: 17px; color: #C2410C; }
.rp-plain { margin: 0; height: 100%; padding: 0; overflow: hidden; } .rp-plain h4 { margin: 4px 0 10px; font-size: 28px; font-weight: 500; letter-spacing: -0.03em; color: #002466; } .rp-plain h4.mt { margin-top: 16px; font-size: 22px; }
.rp-form { background: #fff; border: 1px solid #DCE3EF; border-radius: 16px; padding: 14px 18px; margin-bottom: 4px; } .rp-form h6 { margin: 0 0 10px; font-size: 16px; font-weight: 500; color: #002466; } .rp-fr { display: grid; grid-template-columns: repeat(3, 1fr) auto; gap: 12px; align-items: end; } .rp-fr label { font-size: 12.5px; color: #556182; display: block; margin-bottom: 4px; } .rp-fr i { display: block; font-style: normal; border: 1px solid #DCE3EF; background: #F7F9FC; border-radius: 12px; padding: 10px 12px; color: #8B95AD; } .rp-fr i.v { color: #0A1A40; font-weight: 500; } .rp-form .rp-nb { display: none; }
.rp-added .rp-fr::after { content: "Search"; }
.rp-fr::after { content: attr(data-add); background: #002466; color: #fff; padding: 11px 18px; border-radius: 999px; font-weight: 500; font-size: 13.5px; white-space: nowrap; }
/* patient landing page */
.pp-page { width: 100%; color: #0A1A40; font-family: 'Outfit', system-ui, sans-serif; }
.pp-bar { height: 56px; display: flex; justify-content: space-between; align-items: center; padding: 0 28px; } .pp-bar::before { content: attr(data-org); font-weight: 600; color: #002466; font-size: 17px; } .pp-bar .rp-nb { padding: 9px 20px; background: #002466; color: #fff; }
.pp-hero { margin: 0 20px; border-radius: 24px; padding: 54px 40px; background: radial-gradient(circle at 85% 15%, rgba(135,199,40,.5), transparent 30%), linear-gradient(110deg, #002466, #00184A); color: #fff; display: grid; gap: 10px; }
.pp-hero h5 { margin: 0; font-size: 15px; letter-spacing: .1em; text-transform: uppercase; color: #87C728; font-weight: 500; } .pp-hero p { margin: 0; font-size: 40px; font-weight: 500; letter-spacing: -0.04em; max-width: 14em; line-height: 1.05; } .pp-hero.sm { margin-top: 34px; padding: 30px 40px; } .pp-hero.sm p { font-size: 30px; }
.pp-pill { display: inline-block; margin: 14px 10px 0 0; background: #87C728; color: #00184A; padding: 12px 24px; border-radius: 999px; font-weight: 600; font-size: 16px; } .pp-pill + .pp-pill { background: transparent; color: #fff; border: 1px solid rgba(255,255,255,.4); }
.pp-h { text-align: left; color: #002466; font-size: 30px; font-weight: 500; letter-spacing: -0.03em; margin: 34px 40px 4px; } .pp-s { text-align: left; font-size: 17px; color: #556182; margin: 0 40px 14px; }
.pp-tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 14px 40px 0; } .pp-tile { padding: 24px 20px; border-radius: 20px; min-height: 210px; } .pp-tile.t-a { background: #002466; color: #fff; } .pp-tile.t-b { background: #EEF7DC; color: #002466; } .pp-tile svg { width: 40px; height: 40px; stroke-width: 1.6; color: #87C728; } .pp-tile.t-b svg { color: #4B8010; } .pp-tile h6 { margin: 18px 0 8px; font-size: 19px; font-weight: 500; } .pp-tile p { margin: 0; font-size: 13.5px; line-height: 1.5; opacity: .85; }
.pp-plans { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; padding: 24px 40px 50px; } .pp-plan { border: 1px solid #DCE3EF; border-radius: 22px; padding: 24px 24px 76px; position: relative; color: #0A1A40; min-height: 380px; background: #fff; } .pp-plan.on { background: #002466; color: #fff; border-color: #002466; } .pp-plan svg { position: absolute; right: 22px; top: 22px; width: 40px; height: 40px; stroke-width: 1.6; color: #87C728; } .pp-plan h6 { margin: 0 0 6px; font-size: 21px; font-weight: 500; } .pp-plan .pr em { font-style: normal; font-size: 36px; font-weight: 500; letter-spacing: -0.04em; } .pp-plan .pr small { font-size: 14px; opacity: .7; } .pp-plan .sv { margin: 4px 0 0; font-size: 13.5px; color: #4B8010; font-weight: 500; } .pp-plan.on .sv { color: #87C728; } .pp-plan ul { margin: 14px 0 0; padding-left: 18px; font-size: 13px; line-height: 1.75; } .pp-btn { position: absolute; left: 24px; right: 24px; bottom: 22px; background: #87C728; color: #00184A; text-align: center; padding: 12px 0; border-radius: 999px; font-size: 16px; font-weight: 600; } .pp-plan:not(.on) .pp-btn { background: #002466; color: #fff; }
@keyframes rpIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }
.rp-panel.go .rp-card, .rp-panel.go .rp-stat, .rp-panel.go .rp-modal, .rp-panel.go .pp-tile, .rp-panel.go .pp-plan, .rp-panel.go .rp-form { animation: rpIn .5s ease both; } .rp-panel.go .rp-card:nth-of-type(2), .rp-panel.go .rp-stat:nth-child(2), .rp-panel.go .pp-tile:nth-child(2), .rp-panel.go .pp-plan:nth-child(2) { animation-delay: .1s; } .rp-panel.go .pp-tile:nth-child(3), .rp-panel.go .pp-plan:nth-child(3) { animation-delay: .2s; } .rp-panel.go .pp-tile:nth-child(4) { animation-delay: .3s; }
@media (prefers-reduced-motion: reduce) { .rp-panel.go * { animation: none !important; } .rp-bar { transition: none; } }

/* phones: no scaling, a real mobile layout of the same screens */
@media (max-width: 700px) {
  .rp { width: 100% !important; height: auto; zoom: 1 !important; font-size: 14px; }
  .rp-panel { position: relative; inset: auto; }
  .rp-panel.pp { max-height: 620px; }
  .rp-main { display: block; height: auto; }
  .rp-nav { display: none; }
  .rp-top { height: 52px; padding: 0 14px; } .rp-top img { height: 22px; } .rp-user { font-size: 0; } .rp-user i { font-size: 11px; } .rp-user svg { display: none; }
  .rp-content { padding: 12px 12px 4px; overflow: visible; }
  .rp-ban { height: auto; padding: 18px 18px 18px 82px; border-radius: 16px; } .rp-ban h5 { font-size: 22px; } .rp-ban span { font-size: 11px; }
  .rp-av { left: 26px; top: 26px; width: 48px; height: 48px; border-radius: 13px; font-size: 14px; }
  .rp-acts { margin: 10px 0 0; padding: 0; justify-content: flex-start; } .rp-nb { padding: 9px 14px; font-size: 13px; }
  .rp-row { grid-template-columns: 1fr; gap: 10px; margin-top: 10px; }
  .rp-stats { grid-template-columns: 1fr 1fr; gap: 10px; } .rp-stat { min-height: 0; padding: 14px; } .rp-stat b { font-size: 40px; }
  .rp-chartrow { grid-template-columns: 1fr; } .rp-chart { height: 190px; }
  .rp-card { margin: 10px 0; overflow-x: auto; -webkit-overflow-scrolling: touch; }
  .rp-tb { flex-wrap: wrap; } .rp-btns { display: none; } .rp-in { min-width: 110px; }
  .rp-ft { font-size: 12px; } .rp-pg i { padding: 4px 9px; }
  .rp-dim { display: none; }
  .rp-modal { position: relative; left: auto; top: auto; width: auto; height: auto; margin: 10px 12px 12px; padding: 14px; box-shadow: 0 0 0 1px #DCE3EF; }
  .rp-panel[data-k="member"] .rp-content { display: none; }
  .rp-kv th, .rp-kv td { padding: 7px 10px; font-size: 13px; }
  .rp-plain h4 { font-size: 22px; } .rp-fr { grid-template-columns: 1fr; } .rp-fr::after { justify-self: start; }
  .pp-bar { padding: 0 14px; } .pp-hero { margin: 0 12px; padding: 28px 20px; } .pp-hero p { font-size: 26px; } .pp-hero.sm p { font-size: 20px; }
  .pp-h { margin: 24px 16px 4px; font-size: 22px; } .pp-s { margin: 0 16px 10px; font-size: 15px; }
  .pp-tiles { grid-template-columns: 1fr 1fr; margin: 10px 12px 0; gap: 10px; } .pp-tile { min-height: 0; padding: 16px; } .pp-tile h6 { font-size: 16px; margin-top: 10px; }
  .pp-plans { grid-template-columns: 1fr; padding: 18px 12px 40px; } .pp-plan { min-height: 0; }
  /* tables become stacked cards; chart labels wrap */
  .rp-t.cardify thead { display: none; }
  .rp-t.cardify, .rp-t.cardify tbody { display: block; width: 100%; }
  .rp-t.cardify tr { display: flex !important; flex-direction: column; gap: 2px; padding: 10px 14px; border-top: 1px solid #EDF1F7; }
  .rp-t.cardify td { width: 100%; box-sizing: border-box; }
  .rp-t.cardify tr:first-child { border-top: 0; }
  .rp-t.cardify td { display: flex; justify-content: space-between; align-items: center; gap: 12px; padding: 4px 0; border: 0; background: transparent !important; white-space: normal; text-align: right !important; font-size: 13.5px; }
  .rp-t.cardify td::before { content: attr(data-l); flex: none; font-size: 11.5px; letter-spacing: .05em; text-transform: uppercase; color: #556182; text-align: left; }
  .rp-t.cardify td:first-child { font-weight: 600; color: #002466; }
  .rp-card { overflow-x: visible; }
  .rp-col span { position: static; margin-top: 6px; white-space: normal; text-align: center; font-size: 11px; line-height: 1.2; min-height: 2.4em; }
  .rp-plot { gap: 10px; padding: 0 6px; }
  .rp-chart { height: auto; } .rp-plot { height: 200px; } .rp-y { padding-bottom: 36px; }
  .rp-col { justify-content: flex-end; }
}
"""
