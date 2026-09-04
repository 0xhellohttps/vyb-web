#!/usr/bin/env python3
"""Assemble /Users/b/Projects/vyb-web/forecast.html — VYB revenue forecast for a
promoter integration at three levels. All figures are computed here from the
anonymized baseline (BASELINE) and the assumptions (A) so the page is
internally consistent. Reuses site.css + pulse_extra.css (the /pulse layout)
plus forecast_extra.css.

Baseline figures are a promoter's own trailing results, anonymized and lightly
rounded. The page names no company and no artist.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/Users/b/Projects/vyb-web/forecast.html'

# ---------------------------------------------------------------- baseline (derived from the documents)
BASELINE = {
    'months': 8, 'shows': 64, 'gross': 85.14e6, 'paid_out': 58.39e6, 'profit': 26.75e6, 'attendance': 553604,
    'tiers': [  # name, shows, avg gross, avg paid out, avg attendance, margin
        ('Stadium', 5, 13.83e6, 9.25e6, 67279, .331),
        ('Arena / large room', 11, 861e3, 680e3, 7686, .210),
        ('Theater / club', 30, 203e3, 147e3, 3888, .278),
        ('Small room / activation', 18, 24e3, 14e3, 891, .407),
    ],
    'stadium_run': {'dates': 7, 'budget': 12.385e6, 'artist': 6.5e6, 'production': 2.14e6, 'venue': 1.284e6,
                    'marketing': 856e3, 'personnel': 749e3, 'contingency': 535e3, 'insurance': 321e3,
                    'return': .12, 'repay_days': 100},
    'prior_year': {'gross': 21.9e6, 'profit': 7.0e6},
    'pipeline': {'confirmed': 33, 'on_sale': 26, 'pending': '100+'},
}

# ---------------------------------------------------------------- modeled year (12 months on VYB)
non_stadium_paid_annual = (11*680e3 + 30*147e3 + 18*14e3) / 8 * 12      # ≈ $18.2M
non_stadium_shows_annual = round((11 + 30 + 18) / 8 * 12)               # ≈ 89
CASES = {
    'Low':  {'stadium_dates': 2,  'paid': non_stadium_paid_annual + 2 * 9.25e6,   'shows': non_stadium_shows_annual + 2},
    'Base': {'stadium_dates': 10, 'paid': non_stadium_paid_annual + 10 * 12.385e6, 'shows': non_stadium_shows_annual + 10},
    'High': {'stadium_dates': 14, 'paid': non_stadium_paid_annual * 1.6 + 14 * 12.385e6, 'shows': round(non_stadium_shows_annual * 1.6) + 14},
}
for c in CASES.values():
    c['gross'] = c['paid'] / 0.686   # trailing paid-out / gross ratio

# ---------------------------------------------------------------- assumptions
A = {
    'impl': 25e3,                       # one-time implementation (pitch: $2.5K–$25K)
    'platform_base': 2.5e3 * 12,        # $2,500 / mo (pitch: $250–$2,500 / mo enterprise platform fee)
    'platform_full': 5e3 * 12,          # intelligence + agent layer tier
    'take': 0.0040,                     # blended take on orchestrated payment volume (pitch: 0.25%–1%)
    'card_share': 0.010,                # VYB share of interchange on virtual-card spend
    'card_frac': {'Medium': 0.045, 'Full': 0.065},   # share of paid-out volume that moves to virtual cards
    'routed_q': {'Medium': [.20, .35, .50, .60], 'Full': [.40, .55, .75, .85]},  # share of paid-out volume routed, by quarter
    'routed_y': {'Medium': [None, .65, .75], 'Full': [None, .85, .90]},          # years 2–3
    'adv_per_date': 3.5e6, 'adv_days': 90, 'adv_apr': 0.18, 'orig_fee': 0.01, 'spread_share': 0.35,
    'fin_dates_q': [0, 0, .2, .3],      # share of the year's stadium dates financed through VYB, by quarter (year one)
    'fin_dates_y': [None, .8, .9],
    'hours': {'Stadium': 220, 'Arena / large room': 60, 'Theater / club': 24, 'Small room / activation': 6},
    'hour_cost': 60,
    'hours_saved': {'Base': .40, 'Medium': .70, 'Full': .85},
    'leak': 0.0025,                     # duplicate / over-budget / mis-paid share of routed volume caught
}

def money(x, d=0):
    if abs(x) >= 1e6: return f'${x/1e6:.{1 if d==0 else d}f}M'
    if abs(x) >= 1e3: return f'${x/1e3:.0f}K'
    return f'${x:,.0f}'
def pct(x): return f'{x*100:.0f}%'

def year_one(level, case):
    """Quarterly VYB revenue for level × volume case, plus the exit run-rate and years 2–3."""
    paid = CASES[case]['paid']; dates = CASES[case]['stadium_dates']; qpaid = paid / 4
    rows = []
    for q in range(4):
        r = {'platform': (A['platform_full'] if level == 'Full' else A['platform_base']) / 4,
             'impl': A['impl'] if q == 0 else 0, 'payments': 0, 'cards': 0, 'finance': 0}
        if level in ('Medium', 'Full'):
            routed = A['routed_q'][level][q]
            r['payments'] = qpaid * routed * A['take']
            r['cards'] = qpaid * A['card_frac'][level] * (routed / A['routed_q'][level][3]) * A['card_share']
        if level == 'Full':
            n = dates * A['fin_dates_q'][q]
            interest = A['adv_per_date'] * A['adv_apr'] * A['adv_days'] / 365
            r['finance'] = n * (A['adv_per_date'] * A['orig_fee'] + interest * A['spread_share'])
        r['total'] = sum(v for k, v in r.items())
        rows.append(r)
    y1 = sum(r['total'] for r in rows)
    def full_year(routed, fin_share):
        t = (A['platform_full'] if level == 'Full' else A['platform_base'])
        if level in ('Medium', 'Full'):
            t += paid * routed * A['take'] + paid * A['card_frac'][level] * A['card_share']
        if level == 'Full':
            interest = A['adv_per_date'] * A['adv_apr'] * A['adv_days'] / 365
            t += dates * fin_share * (A['adv_per_date'] * A['orig_fee'] + interest * A['spread_share'])
        return t
    if level == 'Base': y2 = y3 = A['platform_base']
    else:
        y2 = full_year(A['routed_y'][level][1], A['fin_dates_y'][1]); y3 = full_year(A['routed_y'][level][2], A['fin_dates_y'][2])
    exit_rr = full_year(A['routed_q'][level][3] if level != 'Base' else 0, A['fin_dates_q'][3] * 4 if level == 'Full' else 0) if level != 'Base' else A['platform_base']
    return rows, y1, exit_rr, y2, y3

def promoter_value(level, case):
    """What the promoter saves in the modeled year."""
    paid = CASES[case]['paid']; dates = CASES[case]['stadium_dates']
    shows = {'Stadium': dates, 'Arena / large room': round(11/8*12), 'Theater / club': round(30/8*12), 'Small room / activation': round(18/8*12)}
    hours = sum(A['hours'][k] * n for k, n in shows.items())
    v = {'hours': hours, 'hours_saved': hours * A['hours_saved'][level], 'hours_value': hours * A['hours_saved'][level] * A['hour_cost'], 'leak': 0, 'capital': 0}
    if level in ('Medium', 'Full'):
        routed_avg = sum(A['routed_q'][level]) / 4
        v['leak'] = paid * routed_avg * A['leak']
    if level == 'Full':
        n = dates * sum(A['fin_dates_q'])
        today = A['adv_per_date'] * BASELINE['stadium_run']['return']
        vyb = A['adv_per_date'] * A['adv_apr'] * A['adv_days'] / 365 + A['adv_per_date'] * A['orig_fee']
        v['capital'] = n * (today - vyb); v['capital_per_date'] = today - vyb; v['fin_dates'] = n
    v['total'] = v['hours_value'] + v['leak'] + v['capital']
    return v

LEVELS = ['Base', 'Medium', 'Full']
R = {lvl: {c: year_one(lvl, c) for c in CASES} for lvl in LEVELS}
V = {lvl: promoter_value(lvl, 'Base') for lvl in LEVELS}
B = CASES['Base']

# ---------------------------------------------------------------- charts & flowchart (inline SVG, theme-aware via CSS vars)
SERIES = {'Base': 'var(--s1)', 'Medium': 'var(--s2)', 'Full': 'var(--s3)'}

def line_chart():
    W, H, L, Rm, T, Bm = 760, 320, 64, 150, 28, 44
    data = {lvl: [r['total'] for r in R[lvl]['Base'][0]] for lvl in LEVELS}
    ymax = max(max(v) for v in data.values()); step = 100e3; ymax = (int(ymax // step) + 1) * step
    xs = [L + i * (W - L - Rm) / 3 for i in range(4)]
    y = lambda v: T + (H - T - Bm) * (1 - v / ymax)
    s = [f'<svg class="fc-chart" viewBox="0 0 {W} {H}" role="img" aria-labelledby="lc-t" data-chart="line">',
         '<title id="lc-t">VYB revenue by quarter, year one, Base volume</title>']
    for g in range(0, int(ymax) + 1, int(step)):
        s.append(f'<line x1="{L}" x2="{W-Rm}" y1="{y(g):.1f}" y2="{y(g):.1f}" class="grid"/>')
        s.append(f'<text x="{L-10}" y="{y(g)+4:.1f}" class="tick" text-anchor="end">{money(g) if g else "0"}</text>')
    for i, q in enumerate(['Q1', 'Q2', 'Q3', 'Q4']):
        s.append(f'<text x="{xs[i]:.1f}" y="{H-14}" class="tick" text-anchor="middle">{q}</text>')
    for lvl in LEVELS:
        pts = ' '.join(f'{xs[i]:.1f},{y(v):.1f}' for i, v in enumerate(data[lvl]))
        s.append(f'<polyline points="{pts}" fill="none" stroke="{SERIES[lvl]}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
        for i, v in enumerate(data[lvl]):
            s.append(f'<circle cx="{xs[i]:.1f}" cy="{y(v):.1f}" r="4" fill="{SERIES[lvl]}" stroke="var(--bg)" stroke-width="2"/>')
        s.append(f'<text x="{xs[3]+12:.1f}" y="{y(data[lvl][3])+4:.1f}" class="dl">{lvl} · {money(data[lvl][3])}</text>')
    for i in range(4):   # hover columns
        x0 = xs[i] - (xs[1]-xs[0]) / 2; x1 = xs[i] + (xs[1]-xs[0]) / 2
        s.append(f'<rect class="hit" data-i="{i}" x="{max(L, x0):.1f}" y="{T}" width="{min(W-Rm, x1)-max(L, x0):.1f}" height="{H-T-Bm}" fill="transparent"/>')
    s.append('<line class="xh" x1="0" x2="0" y1="%d" y2="%d" stroke="var(--text-tertiary)" stroke-dasharray="3 4" visibility="hidden"/>' % (T, H - Bm))
    s.append('</svg>')
    tip = {'q': ['Q1', 'Q2', 'Q3', 'Q4'], 'series': {lvl: [round(v) for v in data[lvl]] for lvl in LEVELS}, 'x': [round(x, 1) for x in xs]}
    import json as _j
    return '\n'.join(s), _j.dumps(tip)

def bar_chart():
    W, H, L, Rm, T, Bm = 760, 300, 64, 24, 28, 44
    years = ['Year one', 'Year two', 'Year three']
    data = {lvl: [R[lvl]['Base'][1], R[lvl]['Base'][3], R[lvl]['Base'][4]] for lvl in LEVELS}
    ymax = max(max(v) for v in data.values()); step = 500e3; ymax = (int(ymax // step) + 1) * step
    y = lambda v: T + (H - T - Bm) * (1 - v / ymax)
    gw = (W - L - Rm) / 3; bw = 34; gap = 2
    s = [f'<svg class="fc-chart" viewBox="0 0 {W} {H}" role="img" aria-labelledby="bc-t" data-chart="bar">',
         '<title id="bc-t">VYB revenue by year and level, Base volume</title>']
    for g in range(0, int(ymax) + 1, int(step)):
        s.append(f'<line x1="{L}" x2="{W-Rm}" y1="{y(g):.1f}" y2="{y(g):.1f}" class="grid"/>')
        s.append(f'<text x="{L-10}" y="{y(g)+4:.1f}" class="tick" text-anchor="end">{money(g) if g else "0"}</text>')
    for gi, yr in enumerate(years):
        cx = L + gw * gi + gw / 2
        s.append(f'<text x="{cx:.1f}" y="{H-14}" class="tick" text-anchor="middle">{yr}</text>')
        for li, lvl in enumerate(LEVELS):
            v = data[lvl][gi]; x = cx + (li - 1) * (bw + gap) - bw / 2; top = y(v); h = (H - Bm) - top
            s.append(f'<rect class="bar" data-l="{lvl}" data-y="{yr}" data-v="{round(v)}" x="{x:.1f}" y="{top:.1f}" width="{bw}" height="{h:.1f}" rx="4" fill="{SERIES[lvl]}"/>')
            s.append(f'<rect x="{x:.1f}" y="{(H-Bm)-4:.1f}" width="{bw}" height="4" fill="{SERIES[lvl]}"/>')  # square the baseline end
            if lvl == 'Full':
                s.append(f'<text x="{x+bw/2:.1f}" y="{top-8:.1f}" class="dl" text-anchor="middle">{money(v)}</text>')
    s.append(f'<line x1="{L}" x2="{W-Rm}" y1="{H-Bm}" y2="{H-Bm}" class="axis"/>')
    s.append('</svg>')
    return '\n'.join(s)

def legend():
    return '<div class="fc-legend">' + ''.join(f'<span><i style="background:{SERIES[l]}"></i>{l}</span>' for l in LEVELS) + '</div>'

def flowchart():
    def box(x, y, w, h, title, sub='', cls='fb'):
        t = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" class="{cls}"/>'
        if sub:
            t += f'<text x="{x+w/2}" y="{y+h/2-6}" class="ft" text-anchor="middle">{title}</text><text x="{x+w/2}" y="{y+h/2+13}" class="fs" text-anchor="middle">{sub}</text>'
        else:
            t += f'<text x="{x+w/2}" y="{y+h/2+5}" class="ft" text-anchor="middle">{title}</text>'
        return t
    def arrow(x1, y1, x2, y2):
        return f'<path d="M{x1} {y1} L{x2} {y2}" class="fa" marker-end="url(#fc-arr)"/>'
    def tag(x, y, text, lvl):
        return f'<rect x="{x}" y="{y}" width="{len(text)*7.2+18:.0f}" height="22" rx="11" fill="{SERIES[lvl]}"/><text x="{x+9}" y="{y+15}" class="tag">{text}</text>'
    W, H = 900, 560
    s = [f'<svg class="fc-flow" viewBox="0 0 {W} {H}" role="img" aria-labelledby="fl-t">',
         '<title id="fl-t">How money and data move at each integration level</title>',
         '<defs><marker id="fc-arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" class="fah"/></marker></defs>']
    # row 1: the promoter's systems
    srcs = ['Ticketing', 'Bank', 'Accounting', 'Contracts']
    for i, n in enumerate(srcs):
        x = 40 + i * 170; s.append(box(x, 24, 150, 48, n, 'the promoter’s existing system'))
        s.append(arrow(x + 75, 72, x + 75, 108))
    s.append(f'<text x="{40+4*170-20+40}" y="52" class="fs">reads only →</text>')
    # row 2: ledger (Base)
    s.append(box(40, 110, 660, 62, 'VYB event ledger', 'every event a financial object · counterparties · obligations · invoices · approvals · live margin'))
    s.append(tag(720, 130, 'BASE', 'Base'))
    s.append(f'<text x="720" y="172" class="fs">reads everything,</text><text x="720" y="188" class="fs">moves nothing</text>')
    # row 3: policy + router (Medium)
    s.append(arrow(370, 172, 370, 214))
    s.append(box(40, 216, 300, 62, 'Approval policy', 'thresholds · signers · caps · set by the promoter'))
    s.append(box(400, 216, 300, 62, 'Payment router', 'picks the rail · writes the ledger entry'))
    s.append(arrow(340, 247, 398, 247))
    s.append(tag(720, 236, 'MEDIUM', 'Medium'))
    s.append(f'<text x="720" y="278" class="fs">money moves on the</text><text x="720" y="294" class="fs">promoter’s own rails</text>')
    # row 4: rails → counterparties
    s.append(arrow(480, 278, 480, 318)); s.append(arrow(620, 278, 620, 318))
    s.append(box(400, 320, 150, 48, 'Bank rails', 'ACH · wire'))
    s.append(box(560, 320, 140, 48, 'Virtual cards', 'per-persona caps'))
    s.append(arrow(550, 344, 558, 344))
    s.append(arrow(550, 368, 550, 404))
    s.append(box(400, 406, 300, 48, 'Artists · venues · vendors · crews', 'paid in days, reconciled at execution'))
    # Full: agents + capital
    s.append(box(40, 320, 300, 62, 'VYB agents', 'run approvals & settlement inside the policy'))
    s.append(arrow(190, 278, 190, 318))
    s.append(arrow(340, 351, 398, 351))
    s.append(box(40, 406, 300, 62, 'Capital partner', 'advance against contracted receivables'))
    s.append(arrow(190, 382, 190, 404))
    s.append(arrow(340, 430, 398, 430))
    s.append(tag(720, 340, 'FULL', 'Full'))
    s.append(f'<text x="720" y="382" class="fs">agents execute;</text><text x="720" y="398" class="fs">capital repaid from</text><text x="720" y="414" class="fs">the settlement</text>')
    # repayment loop
    s.append(f'<path d="M700 430 C 800 430, 800 500, 560 500 L 190 500 L 190 470" class="fa" marker-end="url(#fc-arr)" stroke-dasharray="4 4"/>')
    s.append(f'<text x="450" y="522" class="fs" text-anchor="middle">box-office settlement repays the advance — automatically, before other distributions</text>')
    s.append('</svg>')
    return '\n'.join(s)

LINE_SVG, LINE_TIP = line_chart()
BAR_SVG = bar_chart()
FLOW_SVG = flowchart()

# ---------------------------------------------------------------- page
css = open(os.path.join(HERE, 'site.css')).read()
extra = open(os.path.join(HERE, 'pulse_extra.css')).read() + open(os.path.join(HERE, 'forecast_extra.css')).read()
js = open(os.path.join(HERE, 'build_pulse.py')).read().split('js = """')[1].split('"""')[0]

def qtable(level):
    rows, y1, rr, y2, y3 = R[level]['Base']
    lines = ['Platform', 'Implementation', 'Payments', 'Cards', 'Financing']
    keys = ['platform', 'impl', 'payments', 'cards', 'finance']
    h = '<table class="fc-table"><thead><tr><th>Year one · Base volume</th><th>Q1</th><th>Q2</th><th>Q3</th><th>Q4</th><th>Year one</th></tr></thead><tbody>'
    for name, k in zip(lines, keys):
        vals = [r[k] for r in rows]
        if sum(vals) == 0: continue
        h += f'<tr><td>{name}</td>' + ''.join(f'<td>{money(x) if x else "—"}</td>' for x in vals) + f'<td><b>{money(sum(vals))}</b></td></tr>'
    h += '<tr class="tot"><td>VYB revenue</td>' + ''.join(f'<td>{money(r["total"])}</td>' for r in rows) + f'<td>{money(y1)}</td></tr>'
    h += '</tbody></table>'
    return h

def kv(rows):
    return '<div class="fc-kv">' + ''.join(f'<div class="fc-kv-row"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in rows) + '</div>'

tiers_html = ''.join(
    f'<tr><td>{n}</td><td>{s}</td><td>{money(g)}</td><td>{money(p)}</td><td>{a:,}</td><td>{pct(m)}</td></tr>'
    for n, s, g, p, a, m in BASELINE['tiers'])
sr = BASELINE['stadium_run']

body = f"""<nav>
  <a href="/" class="nav-logo">
    <span class="app-icon">v</span>
    vyb
  </a>
  <div class="nav-right">
    <a href="/#features" class="nav-link">Features</a>
    <a href="/#enterprise" class="nav-link">Enterprise</a>
    <a href="/pulse" class="nav-link">VYB Pulse</a>
    <a href="/sitemap" class="nav-link">Sitemap</a>
    <a href="mailto:blake@vybapp.io?subject=VYB%20forecast" class="nav-buy-btn">Talk to us</a>
    <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode">
      <span class="tt-icon tt-sun">☀️</span>
      <span class="tt-icon tt-moon">🌙</span>
    </button>
  </div>
</nav>

<div class="pl-page">

<header class="pl-hero" id="top">
  <div class="pl-hero-inner">
    <p class="pl-kicker">Forecast · illustrative</p>
    <h1>Three levels of integration. One promoter's real numbers.</h1>
    <p class="pl-sub">An early revenue forecast for VYB inside an independent live-entertainment promoter's business, built from that promoter's actual show-by-show economics. Three levels — <em>Base</em>, <em>Medium</em>, <em>Full</em> — each modeled on the same twelve months of activity. Every figure on this page is derived from the baseline below and the assumptions at the end; none is a commitment.</p>
    <div class="pl-hero-actions">
      <a href="#levels" class="pl-btn">See the three levels →</a>
      <a href="#assumptions" class="pl-btn-ghost">Read the assumptions</a>
    </div>
    <div class="pl-strip">
      <div><div class="n">{money(B['paid'])}<span class="u">paid out per year · modeled</span></div><div class="l">What the promoter pays artists, venues, vendors and crews in the modeled year.</div></div>
      <div><div class="n">{money(R['Base']['Base'][1])}<span class="u">Base · year one</span></div><div class="l">The event financial control center. Reads everything, moves nothing.</div></div>
      <div><div class="n">{money(R['Medium']['Base'][1])}<span class="u">Medium · year one</span></div><div class="l">Payment orchestration on the promoter's existing rails.</div></div>
      <div><div class="n">{money(R['Full']['Base'][1])}<span class="u">Full · year one</span></div><div class="l">The intelligent operator, with capital against contracted receivables.</div></div>
    </div>
  </div>
</header>

<div class="pl-shell">
  <aside class="pl-rail">
    <div class="pl-rail-h">The forecast</div>
    <div id="plRail" class="pl-rail-nav">
      <a href="#baseline"><span class="i">01</span> The baseline</a>
      <a href="#year"><span class="i">02</span> The modeled year</a>
      <a href="#levels"><span class="i">03</span> Three levels</a>
      <a href="#flow"><span class="i">04</span> How the money moves</a>
      <a href="#base"><span class="i">05</span> Base</a>
      <a href="#medium"><span class="i">06</span> Medium</a>
      <a href="#full"><span class="i">07</span> Full</a>
      <a href="#chart"><span class="i">08</span> Year one by quarter</a>
      <a href="#three"><span class="i">09</span> Three-year view</a>
      <a href="#sensitivity"><span class="i">10</span> Sensitivity</a>
      <a href="#promoter"><span class="i">11</span> The promoter's side</a>
      <a href="#assumptions"><span class="i">12</span> Assumptions</a>
    </div>
  </aside>

  <main class="pl-main">

    <section class="pl-sec" id="baseline">
      <div class="pl-sec-num">01 — THE BASELINE</div>
      <h2 class="pl-h">A promoter that quadrupled in a year.</h2>
      <p class="pl-lede">The subject is an independent promoter and producer headquartered in Las Vegas, operating nightclubs, theaters, arenas, festivals, residencies and a stadium run across a dozen North American markets. The trailing eight months, show by show:</p>
      <div class="fc-stats" data-io="">
        <div><div class="n">{BASELINE['shows']}</div><div class="u">shows · Jan–Aug</div></div>
        <div><div class="n">{money(BASELINE['gross'])}</div><div class="u">gross revenue</div></div>
        <div><div class="n">{money(BASELINE['paid_out'])}</div><div class="u">paid out to counterparties</div></div>
        <div><div class="n">{money(BASELINE['profit'])}</div><div class="u">net profit · {pct(BASELINE['profit']/BASELINE['gross'])} margin</div></div>
        <div><div class="n">{BASELINE['attendance']/1e3:.0f}K</div><div class="u">attendance</div></div>
      </div>
      <div class="fc-table-wrap" data-io="">
        <table class="fc-table">
          <thead><tr><th>Tier</th><th>Shows</th><th>Avg gross</th><th>Avg paid out</th><th>Avg attendance</th><th>Margin</th></tr></thead>
          <tbody>{tiers_html}</tbody>
        </table>
      </div>
      <p class="pl-lede" style="margin-top:26px;">Five stadium dates produced {pct(69.15/85.14)} of the revenue. The other 59 shows are the operating rhythm — a theater or club night every four days, each with its own vendors, crew and settlement. The prior full year grossed {money(BASELINE['prior_year']['gross'])} with {money(BASELINE['prior_year']['profit'])} of profit; the current year passed that by spring.</p>
      <div class="fc-callout" data-io="">
        <div class="fc-callout-h">The stadium run, per date</div>
        <p>Seven further stadium dates are confirmed for the back half of the year, each budgeted at <b>{money(sr['budget'], 2)}</b>: a flat {money(sr['artist'])} artist guarantee ({pct(sr['artist']/sr['budget'])}), {money(sr['production'], 2)} production, {money(sr['venue'], 2)} venue, {money(sr['marketing'])} marketing, {money(sr['personnel'])} personnel and travel, {money(sr['contingency'])} contingency, {money(sr['insurance'])} insurance. Each date is financed show-by-show at a <b>{pct(sr['return'])} fixed return</b> repaid from box-office proceeds within months — {money(sr['budget']*sr['return'], 2)} of cost per date, {money(sr['dates']*sr['budget']*sr['return'])} across the run.</p>
      </div>
      <p class="pl-note">Figures are the promoter's own, lightly rounded. Company and artists are deliberately unnamed. Beyond the confirmed dates sit {BASELINE['pipeline']['on_sale']} shows on sale and {BASELINE['pipeline']['pending']} pending projects, including residencies and national tours, which the High case below draws on.</p>
    </section>

    <section class="pl-sec" id="year">
      <div class="pl-sec-num">02 — THE MODELED YEAR</div>
      <h2 class="pl-h">Twelve months on VYB, in three volume cases.</h2>
      <p class="pl-lede">The forecast runs on <b>paid-out volume</b> — the money the promoter sends to counterparties — because that is what VYB orchestrates and settles. Gross follows at the trailing {pct(0.686)} paid-out-to-gross ratio.</p>
      <div class="fc-table-wrap" data-io="">
        <table class="fc-table">
          <thead><tr><th>Case</th><th>Shows</th><th>Stadium dates</th><th>Paid out</th><th>Gross</th><th>Basis</th></tr></thead>
          <tbody>
            <tr><td>Low</td><td>{CASES['Low']['shows']}</td><td>{CASES['Low']['stadium_dates']}</td><td>{money(CASES['Low']['paid'])}</td><td>{money(CASES['Low']['gross'])}</td><td>The theater, club and arena business annualized, plus two stadium dates.</td></tr>
            <tr class="hi"><td>Base</td><td>{CASES['Base']['shows']}</td><td>{CASES['Base']['stadium_dates']}</td><td>{money(CASES['Base']['paid'])}</td><td>{money(CASES['Base']['gross'])}</td><td>The current year's shape: the same operating rhythm plus ten stadium dates at the confirmed per-date budget.</td></tr>
            <tr><td>High</td><td>{CASES['High']['shows']}</td><td>{CASES['High']['stadium_dates']}</td><td>{money(CASES['High']['paid'])}</td><td>{money(CASES['High']['gross'])}</td><td>Base plus a slice of the pending pipeline: a residency, a national tour, more stadium dates.</td></tr>
          </tbody>
        </table>
      </div>
      <p class="pl-note">Every level below is shown at Base volume. Section 10 re-runs each level at Low and High.</p>
    </section>

    <section class="pl-sec" id="levels">
      <div class="pl-sec-num">03 — THREE LEVELS</div>
      <h2 class="pl-h">The same twelve months, three depths of integration.</h2>
      <p class="pl-lede">Each level contains the one before it. The promoter can stop at any of them; the forecast shows what each is worth to VYB and to the promoter.</p>
      <div class="fc-levels" data-io="">
        <div class="fc-level"><div class="t">Base</div><div class="c">{money(R['Base']['Base'][1])}</div><div class="g">VYB revenue · year one</div><div class="d">Event financial control center. Every event a financial object: counterparties, obligations, invoices, approvals, settlement status, live margin. Reads the promoter's ticketing, bank and accounting; moves nothing.</div><div class="s">Promoter value · {money(V['Base']['total'])}</div></div>
        <div class="fc-level hi"><div class="t">Medium</div><div class="c">{money(R['Medium']['Base'][1])}</div><div class="g">VYB revenue · year one</div><div class="d">Payment orchestration. Vendor, crew, production, marketing and artist payments execute through VYB on the promoter's existing bank rails and virtual cards, under the promoter's approval policy. Reconciled at execution.</div><div class="s">Promoter value · {money(V['Medium']['total'])}</div></div>
        <div class="fc-level"><div class="t">Full</div><div class="c">{money(R['Full']['Base'][1])}</div><div class="g">VYB revenue · year one</div><div class="d">Intelligent event operator. Agents run approvals and settlement within policy, and VYB arranges working capital against contracted receivables — replacing part of the show-by-show financing at a fraction of its cost.</div><div class="s">Promoter value · {money(V['Full']['total'])}</div></div>
      </div>
    </section>


    <section class="pl-sec" id="flow">
      <div class="pl-sec-num">04 — HOW THE MONEY MOVES</div>
      <h2 class="pl-h">One ledger. Three depths.</h2>
      <p class="pl-lede">The promoter's systems stay where they are. At Base, VYB reads them into one event ledger. At Medium, an approval policy and the payment router move money on the promoter's own rails. At Full, agents execute inside the policy and a capital partner advances against contracted receivables, repaid from settlement.</p>
      <div class="fc-flow-wrap" data-io="">{FLOW_SVG}</div>
    </section>
    <section class="pl-sec" id="base">
      <div class="pl-sec-num">05 — BASE</div>
      <h2 class="pl-h">The control center. Small revenue, the foundation for everything after.</h2>
      <p class="pl-lede">At Base, VYB is software: an enterprise platform fee and an implementation. The promoter's {B['shows']} events become {B['shows']} live ledgers, and finance stops rebuilding the settlement in a spreadsheet at load-out.</p>
      <div class="fc-two" data-io="">
        <div>{qtable('Base')}</div>
        <div>
          <div class="pl-sub-h">What the promoter gets</div>
          {kv([('Finance hours today', f"{V['Base']['hours']:,.0f} h / yr across {B['shows']} shows"), ('Hours saved at Base', f"{pct(A['hours_saved']['Base'])} · {V['Base']['hours_saved']:,.0f} h · {money(V['Base']['hours_value'])}"), ('Margin visibility', 'Live, per event, before doors — not at month-end close'), ('Year two', money(R['Base']['Base'][3]) + ' / yr')])}
        </div>
      </div>
    </section>

    <section class="pl-sec" id="medium">
      <div class="pl-sec-num">06 — MEDIUM</div>
      <h2 class="pl-h">Money moves through VYB. Revenue follows the volume.</h2>
      <p class="pl-lede">Routed share ramps from {pct(A['routed_q']['Medium'][0])} of paid-out volume in the first quarter to {pct(A['routed_q']['Medium'][3])} by the fourth — vendors and crews first, then production balances, then artist settlements as the policy has run clean. VYB earns a blended {A['take']*100:.2f}% on orchestrated volume plus a share of interchange on virtual-card spend.</p>
      <div class="fc-two" data-io="">
        <div>{qtable('Medium')}</div>
        <div>
          <div class="pl-sub-h">What the promoter gets</div>
          {kv([('Routed in year one', f"{money(B['paid'] * sum(A['routed_q']['Medium'])/4)} of {money(B['paid'])}"), ('Hours saved', f"{pct(A['hours_saved']['Medium'])} · {money(V['Medium']['hours_value'])}"), ('Leakage caught', f"{money(V['Medium']['leak'])} · duplicates, over-budget lines, mis-paid invoices at {A['leak']*100:.2f}% of routed volume"), ('Vendors paid', 'Days after the show, not weeks; status visible without a call'), ('Year two', money(R['Medium']['Base'][3]) + ' / yr')])}
        </div>
      </div>
    </section>

    <section class="pl-sec" id="full">
      <div class="pl-sec-num">07 — FULL</div>
      <h2 class="pl-h">The operator, and the capital. Where the forecast becomes a business.</h2>
      <p class="pl-lede">Full adds two things. Agents that run approvals and settlement inside the promoter's policy, which lifts routed share to {pct(A['routed_q']['Full'][3])}. And <b>embedded finance</b>: today each stadium date is funded at a {pct(sr['return'])} fixed return repaid within months — roughly {pct(sr['return']*365/sr['repay_days'])} annualized. VYB, with a capital partner, advances {money(A['adv_per_date'])} per date against contracted box-office receivables at {pct(A['adv_apr'])} APR for {A['adv_days']} days, repaid automatically from settlement. VYB keeps a {pct(A['orig_fee'])} origination fee and {pct(A['spread_share'])} of the interest.</p>
      <div class="fc-two" data-io="">
        <div>{qtable('Full')}</div>
        <div>
          <div class="pl-sub-h">What the promoter gets</div>
          {kv([('Hours saved', f"{pct(A['hours_saved']['Full'])} · {money(V['Full']['hours_value'])}"), ('Leakage caught', money(V['Full']['leak'])), ('Cost of capital saved', f"{money(V['Full']['capital_per_date'])} per financed date · {money(V['Full']['capital'])} on {V['Full']['fin_dates']:.0f} dates in year one"), ('At ten dates a year', money(V['Full']['capital_per_date'] * B['stadium_dates']) + ' / yr'), ('Year two', money(R['Full']['Base'][3]) + ' / yr')])}
        </div>
      </div>
      <p class="pl-note">Financing starts in the third quarter, once the ledger has a settlement history to underwrite against: {pct(A['fin_dates_q'][2])} of the year's stadium dates in Q3 and {pct(A['fin_dates_q'][3])} in Q4. The advance covers production and venue deposits, not the artist guarantee.</p>
    </section>


    <section class="pl-sec" id="chart">
      <div class="pl-sec-num">08 — YEAR ONE, BY QUARTER</div>
      <h2 class="pl-h">Revenue follows adoption, then the stadium calendar.</h2>
      <p class="pl-lede">Base is flat after the implementation quarter. Medium climbs with routed share. Full steps up in the third quarter, when financing starts against a settlement history the ledger has by then earned.</p>
      <div class="fc-chart-wrap" data-io="">{legend()}{LINE_SVG}<div class="fc-tip" id="fcTip" hidden></div></div>
      <p class="pl-note">Hover a quarter for the three values. The table in each level's section carries the same numbers.</p>
    </section>

    <section class="pl-sec" id="three">
      <div class="pl-sec-num">09 — THREE-YEAR VIEW</div>
      <h2 class="pl-h">Same promoter, same volume, deeper adoption.</h2>
      <p class="pl-lede">Volume is held flat at Base to isolate adoption. Routed share settles at {pct(A['routed_y']['Medium'][2])} (Medium) and {pct(A['routed_y']['Full'][2])} (Full); financed stadium dates at {pct(A['fin_dates_y'][2])} of the run.</p>
      <div class="fc-chart-wrap" data-io="">{legend()}{BAR_SVG}</div>
      <div class="fc-table-wrap" data-io="">
        <table class="fc-table">
          <thead><tr><th>VYB revenue</th><th>Year one</th><th>Year two</th><th>Year three</th></tr></thead>
          <tbody>
            {''.join(f'<tr{" class=hi" if lvl=="Full" else ""}><td>{lvl}</td><td>{money(R[lvl]["Base"][1])}</td><td>{money(R[lvl]["Base"][3])}</td><td>{money(R[lvl]["Base"][4])}</td></tr>' for lvl in LEVELS)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="pl-sec" id="sensitivity">
      <div class="pl-sec-num">10 — SENSITIVITY</div>
      <h2 class="pl-h">Year-one revenue across the three volume cases.</h2>
      <div class="fc-table-wrap" data-io="">
        <table class="fc-table">
          <thead><tr><th>Year one</th><th>Low · {money(CASES['Low']['paid'])} paid out</th><th>Base · {money(CASES['Base']['paid'])}</th><th>High · {money(CASES['High']['paid'])}</th></tr></thead>
          <tbody>
            {''.join(f'<tr><td>{lvl}</td>' + ''.join(f'<td>{money(R[lvl][c][1])}</td>' for c in CASES) + '</tr>' for lvl in LEVELS)}
          </tbody>
        </table>
      </div>
      <p class="pl-lede" style="margin-top:26px;">Base level is insensitive to volume — it is a software fee. Medium scales with the money that moves. Full scales with the money and with the stadium calendar, because that is where the financing lives.</p>
    </section>

    <section class="pl-sec" id="promoter">
      <div class="pl-sec-num">11 — THE PROMOTER'S SIDE</div>
      <h2 class="pl-h">At every level the promoter keeps more than VYB earns.</h2>
      <div class="fc-table-wrap" data-io="">
        <table class="fc-table">
          <thead><tr><th>Year one · Base volume</th><th>Base</th><th>Medium</th><th>Full</th></tr></thead>
          <tbody>
            <tr><td>Finance hours saved</td>{''.join(f"<td>{money(V[l]['hours_value'])}</td>" for l in LEVELS)}</tr>
            <tr><td>Leakage caught</td>{''.join(f"<td>{money(V[l]['leak']) if V[l]['leak'] else '—'}</td>" for l in LEVELS)}</tr>
            <tr><td>Cost of capital saved</td>{''.join(f"<td>{money(V[l]['capital']) if V[l]['capital'] else '—'}</td>" for l in LEVELS)}</tr>
            <tr class="tot"><td>Promoter value</td>{''.join(f"<td>{money(V[l]['total'])}</td>" for l in LEVELS)}</tr>
            <tr><td>VYB revenue</td>{''.join(f"<td>{money(R[l]['Base'][1])}</td>" for l in LEVELS)}</tr>
            <tr><td>Value per VYB dollar</td>{''.join(f"<td>{V[l]['total']/R[l]['Base'][1]:.1f}×</td>" for l in LEVELS)}</tr>
          </tbody>
        </table>
      </div>
      <p class="pl-lede" style="margin-top:26px;">Not counted: settlement moving from weeks to the night of the show, vendor inquiries falling to near zero, margin known before doors, and the promoter's finance team reading one ledger instead of six systems.</p>
    </section>

    <section class="pl-sec" id="assumptions">
      <div class="pl-sec-num">12 — ASSUMPTIONS</div>
      <h2 class="pl-h">Every number above traces to one of these.</h2>
      <div class="pl-rows">
        <div class="pl-row" data-io=""><div class="r-i">01</div><div class="r-t">Pricing</div><div class="r-d">Implementation {money(A['impl'])} one-time. Platform {money(A['platform_base']/12)} / month at Base and Medium, {money(A['platform_full']/12)} / month at Full for the agent and intelligence layer. Payments {A['take']*100:.2f}% blended on orchestrated volume. Virtual cards: VYB keeps {pct(A['card_share'])} of spend as its share of interchange, on {pct(A['card_frac']['Medium'])}–{pct(A['card_frac']['Full'])} of paid-out volume moving to cards. All within the ranges on the VYB pitch.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">02</div><div class="r-t">Adoption</div><div class="r-d">Routed share of paid-out volume by quarter: Medium {' → '.join(pct(x) for x in A['routed_q']['Medium'])}; Full {' → '.join(pct(x) for x in A['routed_q']['Full'])}. Years two and three: Medium {pct(A['routed_y']['Medium'][1])}, {pct(A['routed_y']['Medium'][2])}; Full {pct(A['routed_y']['Full'][1])}, {pct(A['routed_y']['Full'][2])}. Artist guarantees are the last category to move.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">03</div><div class="r-t">Financing</div><div class="r-d">{money(A['adv_per_date'])} advanced per stadium date against contracted receivables for {A['adv_days']} days at {pct(A['adv_apr'])} APR; VYB earns a {pct(A['orig_fee'])} origination fee and {pct(A['spread_share'])} of interest, the capital partner the rest. Compared against the promoter's current {pct(sr['return'])} fixed return per date. Financed dates: none in H1, {pct(A['fin_dates_q'][2])} of the year's dates in Q3, {pct(A['fin_dates_q'][3])} in Q4; {pct(A['fin_dates_y'][1])} and {pct(A['fin_dates_y'][2])} in years two and three.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">04</div><div class="r-t">Finance workload</div><div class="r-d">Hours of finance and admin per show today — stadium {A['hours']['Stadium']}, arena {A['hours']['Arena / large room']}, theater or club {A['hours']['Theater / club']}, small room {A['hours']['Small room / activation']} — at a {money(A['hour_cost'])} loaded hourly cost. Saved: {pct(A['hours_saved']['Base'])} at Base, {pct(A['hours_saved']['Medium'])} at Medium, {pct(A['hours_saved']['Full'])} at Full.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">05</div><div class="r-t">Leakage</div><div class="r-d">{A['leak']*100:.2f}% of routed volume caught as duplicate invoices, over-budget lines or mis-paid amounts before payment. Conservative against industry reconciliation experience; counted only on volume that actually routes through VYB.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">06</div><div class="r-t">Volume</div><div class="r-d">Non-stadium activity annualized from the trailing eight months ({money(non_stadium_paid_annual)} paid out across {non_stadium_shows_annual} shows). Stadium dates at the confirmed {money(sr['budget'], 2)} per-date budget. Gross at the trailing {pct(0.686)} paid-out-to-gross ratio. Volume held flat across the three-year view.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">07</div><div class="r-t">What this is not</div><div class="r-d">Not an offer, a quote or a commitment by either party. Pricing, adoption and financing terms are a conversation; this page is the shape of one. Figures are the promoter's own trailing results, lightly rounded and unnamed.</div></div>
      </div>
      <div class="pl-cta" style="margin-top:40px;">
        <div class="pl-cta-card" data-io=""><h3>Run it on your numbers</h3><p>Send a show-by-show P&amp;L and the model comes back with your own three levels.</p><a href="mailto:blake@vybapp.io?subject=VYB%20forecast">blake@vybapp.io →</a></div>
        <div class="pl-cta-card" data-io=""><h3>See the operating system</h3><p>The product behind the forecast: the ledger, the agent, the payment router.</p><a href="/#features">Features →</a></div>
      </div>
    </section>

  </main>
</div>
</div>

<footer>
  <div class="footer-inner">
    <div>
      <div class="footer-brand"><span class="app-icon">v</span> vyb</div>
      <div class="footer-meta">© 2026 VYB · FORECAST · ILLUSTRATIVE</div>
    </div>
    <div class="footer-links">
      <a href="/">Home</a>
      <a href="/#enterprise">Enterprise</a>
      <a href="/pulse">VYB Pulse</a>
      <a href="mailto:blake@vybapp.io?subject=VYB%20forecast">Contact</a>
    </div>
  </div>
</footer>
"""

TITLE = "VYB — Forecast"
DESC = "An early revenue forecast for VYB integrated into an independent live-entertainment promoter at three levels — Base, Medium and Full — built from the promoter's real show-by-show economics."
page = f"""<!DOCTYPE html>
<html lang="en" data-theme="light"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#ffffff" id="themeColorMeta">
<meta name="color-scheme" content="light dark">
<meta name="robots" content="noindex">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://vybapp.io/forecast">
<link rel="canonical" href="https://vybapp.io/forecast">
<style>{css}{extra}</style>
</head>
<body>
{body}
<script>
{js}
(function(){{
  var tip=document.getElementById('fcTip'), svg=document.querySelector('svg[data-chart=line]'); if(!tip||!svg) return;
  var D={LINE_TIP}; var xh=svg.querySelector('.xh');
  function fmt(v){{return v>=1e6?'$'+(v/1e6).toFixed(1)+'M':'$'+Math.round(v/1e3)+'K';}}
  svg.querySelectorAll('.hit').forEach(function(r){{
    r.addEventListener('mouseenter',function(){{var i=+r.dataset.i; xh.setAttribute('x1',D.x[i]); xh.setAttribute('x2',D.x[i]); xh.setAttribute('visibility','visible');
      tip.innerHTML='<b>'+D.q[i]+'</b>'+Object.keys(D.series).map(function(k){{return '<span>'+k+' <em>'+fmt(D.series[k][i])+'</em></span>';}}).join(''); tip.hidden=false;
      var b=svg.getBoundingClientRect(), w=svg.parentNode.getBoundingClientRect(); var px=(D.x[i]/760)*b.width+(b.left-w.left); tip.style.left=Math.min(px,w.width-190)+'px';}});
    r.addEventListener('mouseleave',function(){{tip.hidden=true; xh.setAttribute('visibility','hidden');}});
  }});
  document.querySelectorAll('svg[data-chart=bar] .bar').forEach(function(b){{ var t=document.createElementNS('http://www.w3.org/2000/svg','title'); t.textContent=b.dataset.l+' \u00b7 '+b.dataset.y+' \u00b7 '+fmt(+b.dataset.v); b.appendChild(t); }});
}})();
</script>
</body></html>
"""
open(OUT, 'w', encoding='utf-8').write(page)
print(f"wrote {OUT} ({len(page)} bytes)")
for lvl in LEVELS:
    rows, y1, rr, y2, y3 = R[lvl]['Base']
    print(f"{lvl:6s} Y1 {money(y1):>8s}  exit {money(rr):>8s}  Y2 {money(y2):>8s}  Y3 {money(y3):>8s} | promoter value {money(V[lvl]['total']):>8s} | Low {money(R[lvl]['Low'][1]):>7s} High {money(R[lvl]['High'][1]):>7s}")
print('cases:', {k: (v['shows'], money(v['paid']), money(v['gross'])) for k, v in CASES.items()})
