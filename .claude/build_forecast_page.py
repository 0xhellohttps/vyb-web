# Page half of the forecast build. Imported by build_forecast.py after the model
# (BASELINE, CASES, A, R, V, B, LEVELS, money, pct) is in scope via exec.
import os, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/Users/b/Projects/vyb-web/forecast.html'
sr = BASELINE['stadium_run']
TPV = B['paid']

# ---------------------------------------------------------------- derived investor metrics
Y1 = {lvl: R[lvl]['Base'][1] for lvl in LEVELS}
Y2 = {lvl: R[lvl]['Base'][3] for lvl in LEVELS}
Y3 = {lvl: R[lvl]['Base'][4] for lvl in LEVELS}
take_bps = {lvl: Y1[lvl] / TPV * 1e4 for lvl in LEVELS}
per_1m = {lvl: Y1[lvl] / (TPV / 1e6) for lvl in LEVELS}
mult = {'bm': Y1['Medium'] / Y1['Base'], 'bf': Y1['Full'] / Y1['Base'], 'mf': Y1['Full'] / Y1['Medium']}
full_rows = R['Full']['Base'][0]
STREAMS = [('Platform', 'platform'), ('Implementation', 'impl'), ('Payments', 'payments'), ('Cards', 'cards'), ('Financing', 'finance')]
stream_y1 = {k: sum(r[k] for r in full_rows) for _, k in STREAMS}
routed_y1 = {lvl: TPV * sum(A['routed_q'][lvl]) / 4 for lvl in ('Medium', 'Full')}
routed_y3 = {lvl: TPV * A['routed_y'][lvl][2] for lvl in ('Medium', 'Full')}
fin_dates_y1 = B['stadium_dates'] * sum(A['fin_dates_q'])
fin_vol_y1 = fin_dates_y1 * A['adv_per_date']
fin_vol_rr = B['stadium_dates'] * A['adv_per_date']
interest_per_date = A['adv_per_date'] * A['adv_apr'] * A['adv_days'] / 365
vyb_per_date = A['adv_per_date'] * A['orig_fee'] + interest_per_date * A['spread_share']
today_per_date = A['adv_per_date'] * sr['return']
# gross-margin assumptions per stream (modeled)
GM = {'platform': .85, 'impl': .60, 'payments': .70, 'cards': .80, 'finance': .90}
gp_stream = {k: stream_y1[k] * GM[k] for k in stream_y1}
gp_full = sum(gp_stream.values())
gp_level = {lvl: sum(sum(r[k] for r in R[lvl]['Base'][0]) * GM[k] for k in GM) for lvl in LEVELS}
SCALE = [1, 10, 25, 50, 100]

def bps(x): return f'{x:.1f} bps'
def mx(x): return f'{x:.1f}×'

# ---------------------------------------------------------------- palette & svg helpers
S1, S2, S3, S4, S5 = 'var(--s1)', 'var(--s2)', 'var(--s3)', 'var(--s4)', 'var(--s5)'
SERIES = {'Base': S1, 'Medium': S2, 'Full': S3}
STREAM_COL = {'platform': S1, 'impl': S4, 'payments': S2, 'cards': S5, 'finance': S3}

def line_chart():
    W, H, L, Rm, T, Bm = 760, 320, 64, 150, 28, 44
    data = {lvl: [r['total'] for r in R[lvl]['Base'][0]] for lvl in LEVELS}
    ymax = max(max(v) for v in data.values()); step = 100e3; ymax = (int(ymax // step) + 1) * step
    xs = [L + i * (W - L - Rm) / 3 for i in range(4)]
    y = lambda v: T + (H - T - Bm) * (1 - v / ymax)
    s = [f'<svg class="fc-chart" viewBox="0 0 {W} {H}" role="img" aria-labelledby="lc-t" data-chart="line"><title id="lc-t">VYB revenue by quarter, year one, Base volume</title>']
    for g in range(0, int(ymax) + 1, int(step)):
        s.append(f'<line x1="{L}" x2="{W-Rm}" y1="{y(g):.1f}" y2="{y(g):.1f}" class="grid"/><text x="{L-10}" y="{y(g)+4:.1f}" class="tick" text-anchor="end">{money(g) if g else "0"}</text>')
    for i, q in enumerate(['Q1', 'Q2', 'Q3', 'Q4']):
        s.append(f'<text x="{xs[i]:.1f}" y="{H-14}" class="tick" text-anchor="middle">{q}</text>')
    for lvl in LEVELS:
        pts = ' '.join(f'{xs[i]:.1f},{y(v):.1f}' for i, v in enumerate(data[lvl]))
        s.append(f'<polyline points="{pts}" fill="none" stroke="{SERIES[lvl]}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
        for i, v in enumerate(data[lvl]):
            s.append(f'<circle cx="{xs[i]:.1f}" cy="{y(v):.1f}" r="4" fill="{SERIES[lvl]}" stroke="var(--bg)" stroke-width="2"/>')
        s.append(f'<text x="{xs[3]+12:.1f}" y="{y(data[lvl][3])+4:.1f}" class="dl">{lvl} · {money(data[lvl][3])}</text>')
    for i in range(4):
        x0 = xs[i] - (xs[1]-xs[0]) / 2; x1 = xs[i] + (xs[1]-xs[0]) / 2
        s.append(f'<rect class="hit" data-i="{i}" x="{max(L, x0):.1f}" y="{T}" width="{min(W-Rm, x1)-max(L, x0):.1f}" height="{H-T-Bm}" fill="transparent"/>')
    s.append(f'<line class="xh" x1="0" x2="0" y1="{T}" y2="{H-Bm}" stroke="var(--text-tertiary)" stroke-dasharray="3 4" visibility="hidden"/></svg>')
    tip = {'q': ['Q1', 'Q2', 'Q3', 'Q4'], 'series': {lvl: [round(v) for v in data[lvl]] for lvl in LEVELS}, 'x': [round(x, 1) for x in xs]}
    return '\n'.join(s), json.dumps(tip)

def bar_chart():
    W, H, L, Rm, T, Bm = 760, 300, 64, 24, 28, 44
    years = ['Year one', 'Year two', 'Year three']
    data = {lvl: [Y1[lvl], Y2[lvl], Y3[lvl]] for lvl in LEVELS}
    ymax = max(max(v) for v in data.values()); step = 500e3; ymax = (int(ymax // step) + 1) * step
    y = lambda v: T + (H - T - Bm) * (1 - v / ymax)
    gw = (W - L - Rm) / 3; bw = 34; gap = 2
    s = [f'<svg class="fc-chart" viewBox="0 0 {W} {H}" role="img" aria-labelledby="bc-t" data-chart="bar"><title id="bc-t">VYB revenue by year and level, Base volume</title>']
    for g in range(0, int(ymax) + 1, int(step)):
        s.append(f'<line x1="{L}" x2="{W-Rm}" y1="{y(g):.1f}" y2="{y(g):.1f}" class="grid"/><text x="{L-10}" y="{y(g)+4:.1f}" class="tick" text-anchor="end">{money(g) if g else "0"}</text>')
    for gi, yr in enumerate(years):
        cx = L + gw * gi + gw / 2
        s.append(f'<text x="{cx:.1f}" y="{H-14}" class="tick" text-anchor="middle">{yr}</text>')
        for li, lvl in enumerate(LEVELS):
            v = data[lvl][gi]; x = cx + (li - 1) * (bw + gap) - bw / 2; top = y(v); h = (H - Bm) - top
            s.append(f'<rect class="bar" data-l="{lvl}" data-y="{yr}" data-v="{round(v)}" x="{x:.1f}" y="{top:.1f}" width="{bw}" height="{h:.1f}" rx="4" fill="{SERIES[lvl]}"/><rect x="{x:.1f}" y="{(H-Bm)-4:.1f}" width="{bw}" height="4" fill="{SERIES[lvl]}"/>')
            if lvl == 'Full': s.append(f'<text x="{x+bw/2:.1f}" y="{top-8:.1f}" class="dl" text-anchor="middle">{money(v)}</text>')
    s.append(f'<line x1="{L}" x2="{W-Rm}" y1="{H-Bm}" y2="{H-Bm}" class="axis"/></svg>')
    return '\n'.join(s)

def legend(items):
    return '<div class="fc-legend">' + ''.join(f'<span><i style="background:{c}"></i>{l}</span>' for l, c in items) + '</div>'

def donut():
    total = sum(stream_y1.values()); cx = cy = 110; r = 84; sw = 26; circ = 2 * math.pi * r
    s = [f'<svg class="fc-donut" viewBox="0 0 220 220" role="img" aria-labelledby="dn-t"><title id="dn-t">Full integration revenue mix, year one</title>']
    off = 0
    for name, k in STREAMS:
        frac = stream_y1[k] / total; dash = circ * frac
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{STREAM_COL[k]}" stroke-width="{sw}" stroke-dasharray="{max(dash-3,0):.2f} {circ-max(dash-3,0):.2f}" stroke-dashoffset="{-off:.2f}" transform="rotate(-90 {cx} {cy})"><title>{name} · {money(stream_y1[k])} · {pct(frac)}</title></circle>')
        off += dash
    s.append(f'<text x="{cx}" y="{cy-4}" class="dn-n" text-anchor="middle">{money(total)}</text><text x="{cx}" y="{cy+16}" class="dn-s" text-anchor="middle">Full · year one</text></svg>')
    return '\n'.join(s)

def stack_bar():
    total = sum(stream_y1.values()); W = 760; H = 64
    s = [f'<svg class="fc-stack" viewBox="0 0 {W} {H}" role="img" aria-labelledby="st-t"><title id="st-t">Full integration revenue stack, year one</title>']
    x = 0
    for name, k in STREAMS:
        w = W * stream_y1[k] / total
        s.append(f'<rect x="{x+1:.1f}" y="10" width="{max(w-2,0):.1f}" height="28" rx="4" fill="{STREAM_COL[k]}"><title>{name} · {money(stream_y1[k])}</title></rect>')
        if w > 70: s.append(f'<text x="{x+w/2:.1f}" y="58" class="tick" text-anchor="middle">{name} · {money(stream_y1[k])}</text>')
        x += w
    s.append('</svg>')
    return '\n'.join(s)

def flywheel():
    nodes = ['More events', 'More transaction volume', 'More money routed through VYB', 'Payments, cards, financing', 'More VYB revenue', 'Transaction and data intelligence', 'Better underwriting and products', 'More capital deployed', 'More customer value']
    n = len(nodes); cx = cy = 320; R0 = 232
    s = ['<div class="fc-fly"><svg viewBox="0 0 640 640" aria-hidden="true"><defs><marker id="fw-a" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--accent)"/></marker></defs>',
         f'<circle cx="{cx}" cy="{cy}" r="{R0}" fill="none" stroke="var(--surface-border)" stroke-width="1.5"/>',
         f'<path d="M {cx} {cy-R0} A {R0} {R0} 0 1 1 {cx-70:.0f} {cy-R0+11:.0f}" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-linecap="round" marker-end="url(#fw-a)" stroke-dasharray="10 10" opacity="0.85"/></svg>',
         '<div class="fw-c"><div class="t">The capital flywheel</div><div class="s">Transactions → data → underwriting → financing → more transactions.</div></div>']
    for i, lab in enumerate(nodes):
        a = -math.pi / 2 + 2 * math.pi * i / n; x = 50 + 50 * (R0 / 320) * math.cos(a); y = 50 + 50 * (R0 / 320) * math.sin(a)
        s.append(f'<div class="fw-n" style="left:{x:.1f}%;top:{y:.1f}%;"><div class="b">{i+1}</div><div class="l">{lab}</div></div>')
    s.append('</div>')
    return '\n'.join(s)

def heatmap():
    vals = {lvl: {c: R[lvl][c][1] for c in CASES} for lvl in LEVELS}
    vmax = max(v for d in vals.values() for v in d.values())
    h = ['<div class="fc-heat"><div class="hd"></div>'] + [f'<div class="hd">{c} · {money(CASES[c]["paid"])}</div>' for c in CASES]
    for lvl in LEVELS:
        h.append(f'<div class="hl">{lvl}</div>')
        for c in CASES:
            v = vals[lvl][c]; a = 0.08 + 0.55 * (v / vmax) ** 0.6
            h.append(f'<div class="hc" style="--a:{a:.2f}"><b>{money(v)}</b><span>{v/CASES[c]["paid"]*1e4:.0f} bps</span></div>')
    h.append('</div>')
    return ''.join(h)

def flowchart():
    def box(x, y, w, h, title, sub=''):
        t = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" class="fb"/>'
        if sub: t += f'<text x="{x+w/2}" y="{y+h/2-6}" class="ft" text-anchor="middle">{title}</text><text x="{x+w/2}" y="{y+h/2+13}" class="fs" text-anchor="middle">{sub}</text>'
        else: t += f'<text x="{x+w/2}" y="{y+h/2+5}" class="ft" text-anchor="middle">{title}</text>'
        return t
    def arrow(x1, y1, x2, y2): return f'<path d="M{x1} {y1} L{x2} {y2}" class="fa" marker-end="url(#fc-arr)"/>'
    def tag(x, y, text, col): return f'<rect x="{x}" y="{y}" width="{len(text)*7.2+18:.0f}" height="22" rx="11" fill="{col}"/><text x="{x+9}" y="{y+15}" class="tag">{text}</text>'
    s = ['<svg class="fc-flow" viewBox="0 0 900 560" role="img" aria-labelledby="fl-t"><title id="fl-t">How money and data move at each integration level</title><defs><marker id="fc-arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" class="fah"/></marker></defs>']
    for i, n in enumerate(['Ticketing', 'Bank', 'Accounting', 'Contracts']):
        x = 40 + i * 170; s.append(box(x, 24, 150, 48, n, 'the customer’s existing system')); s.append(arrow(x + 75, 72, x + 75, 108))
    s.append('<text x="720" y="52" class="fs">reads only →</text>')
    s.append(box(40, 110, 660, 62, 'VYB event ledger', 'every event a financial object · counterparties · obligations · invoices · approvals · live margin')); s.append(tag(720, 130, 'BASE', S1))
    s.append('<text x="720" y="172" class="fs">reads everything,</text><text x="720" y="188" class="fs">moves nothing</text>')
    s.append(arrow(370, 172, 370, 214)); s.append(box(40, 216, 300, 62, 'Approval policy', 'thresholds · signers · caps · set by the customer')); s.append(box(400, 216, 300, 62, 'Payment router', 'picks the rail · writes the ledger entry')); s.append(arrow(340, 247, 398, 247))
    s.append(tag(720, 236, 'MEDIUM', S2)); s.append('<text x="720" y="278" class="fs">money moves on the</text><text x="720" y="294" class="fs">customer’s own rails</text>')
    s.append(arrow(480, 278, 480, 318)); s.append(arrow(620, 278, 620, 318)); s.append(box(400, 320, 150, 48, 'Bank rails', 'ACH · wire')); s.append(box(560, 320, 140, 48, 'Virtual cards', 'per-persona caps')); s.append(arrow(550, 344, 558, 344)); s.append(arrow(550, 368, 550, 404))
    s.append(box(400, 406, 300, 48, 'Artists · venues · vendors · crews', 'paid in days, reconciled at execution'))
    s.append(box(40, 320, 300, 62, 'VYB agents', 'run approvals & settlement inside the policy')); s.append(arrow(190, 278, 190, 318)); s.append(arrow(340, 351, 398, 351))
    s.append(box(40, 406, 300, 62, 'Capital partner', 'funds the advance · VYB originates and services')); s.append(arrow(190, 382, 190, 404)); s.append(arrow(340, 430, 398, 430))
    s.append(tag(720, 340, 'FULL', S3)); s.append('<text x="720" y="382" class="fs">agents execute;</text><text x="720" y="398" class="fs">capital repaid from</text><text x="720" y="414" class="fs">the settlement</text>')
    s.append('<path d="M700 430 C 800 430, 800 500, 560 500 L 190 500 L 190 470" class="fa" marker-end="url(#fc-arr)" stroke-dasharray="4 4"/><text x="450" y="522" class="fs" text-anchor="middle">box-office settlement repays the advance — automatically, before other distributions</text></svg>')
    return '\n'.join(s)

LINE_SVG, LINE_TIP = line_chart(); BAR_SVG = bar_chart(); DONUT = donut(); STACK = stack_bar(); FLY = flywheel(); HEAT = heatmap(); FLOW = flowchart()

# ---------------------------------------------------------------- html helpers
def kpi(n, u, l=''):
    return f'<div class="kpi"><div class="n">{n}</div><div class="u">{u}</div>{f"<div class=l>{l}</div>" if l else ""}</div>'
def kv(rows):
    return '<div class="fc-kv">' + ''.join(f'<div class="fc-kv-row"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in rows) + '</div>'
def qtable(level):
    rows, y1, rr, y2, y3 = R[level]['Base']
    h = '<table class="fc-table"><thead><tr><th>Year one · Base volume</th><th>Q1</th><th>Q2</th><th>Q3</th><th>Q4</th><th>Year one</th></tr></thead><tbody>'
    for name, k in STREAMS:
        vals = [r[k] for r in rows]
        if sum(vals) == 0: continue
        h += f'<tr><td>{name}</td>' + ''.join(f'<td>{money(x) if x else "—"}</td>' for x in vals) + f'<td><b>{money(sum(vals))}</b></td></tr>'
    h += '<tr class="tot"><td>VYB revenue</td>' + ''.join(f'<td>{money(r["total"])}</td>' for r in rows) + f'<td>{money(y1)}</td></tr></tbody></table>'
    return h

tiers_html = ''.join(f'<tr><td>{n}</td><td>{s}</td><td>{money(g)}</td><td>{money(p)}</td><td>{a:,}</td><td>{pct(m)}</td></tr>' for n, s, g, p, a, m in BASELINE['tiers'])
DATE_ROWS = [
    ('Artist guarantee', sr['artist'], 'Tracked as one obligation: deposit, balance, due dates, status', 'Wire · routed last, from Q4', 'Two signatures — finance lead, then principal'),
    ('Production', sr['production'], 'Tracked line by line as vendor obligations', 'ACH · routed from Q2; change orders flagged before approval', 'Inside the financed slice; agents approve within caps'),
    ('Venue', sr['venue'], 'Tracked: deposit, balance, ancillary share', 'Wire · routed from Q2', 'Inside the financed slice'),
    ('Marketing', sr['marketing'], 'Tracked against the campaign budget', 'ACH and virtual cards · routed from Q1', 'Agents execute under the campaign cap'),
    ('Personnel and travel', sr['personnel'], 'Tracked per payee', 'Virtual cards and ACH · routed from Q1', 'Cross-border crew on a stablecoin rail, shown as dollars'),
    ('Contingency', sr['contingency'], 'Tracked as a reserve', 'Held; released on approval', 'Agent proposes the release'),
    ('Insurance and permits', sr['insurance'], 'Tracked', 'ACH · routed from Q1', 'Unchanged'),
]
date_rows_html = ''.join(f'<tr><td>{c}</td><td>{money(a, 2) if a >= 1e6 else money(a)}</td><td>{b}</td><td>{m}</td><td>{f}</td></tr>' for c, a, b, m, f in DATE_ROWS)
scale_rows = ''.join(f'<tr{" class=hi" if n==1 else ""}><td>{n}</td><td>{money(n*TPV)}</td><td>{money(n*Y1["Medium"])}</td><td>{money(n*Y1["Full"])}</td><td>{money(n*Y3["Full"])}</td></tr>' for n in SCALE)
unit_rows = ''.join(f'<tr><td>{name}</td><td>{money(stream_y1[k])}</td><td>{pct(GM[k])}</td><td>{money(gp_stream[k])}</td><td class="m">{note}</td></tr>' for (name, k), note in zip(STREAMS, ['hosting, support, success', 'services delivery', 'rail and network costs, ~0.12% of routed volume', 'network and program costs', 'servicing; funding cost sits with the capital partner']))

css = open(os.path.join(HERE, 'site.css')).read()
extra = open(os.path.join(HERE, 'pulse_extra.css')).read() + open(os.path.join(HERE, 'forecast_extra.css')).read()
js = open(os.path.join(HERE, 'build_pulse.py')).read().split('js = """')[1].split('"""')[0]

body = f"""<nav>
  <a href="/" class="nav-logo"><span class="app-icon">v</span> vyb</a>
  <div class="nav-right">
    <a href="/#features" class="nav-link">Features</a>
    <a href="/#enterprise" class="nav-link">Enterprise</a>
    <a href="/pulse" class="nav-link">VYB Pulse</a>
    <a href="/sitemap" class="nav-link">Sitemap</a>
    <a href="mailto:blake@vybapp.io?subject=VYB%20forecast" class="nav-buy-btn">Talk to us</a>
    <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode"><span class="tt-icon tt-sun">☀️</span><span class="tt-icon tt-moon">🌙</span></button>
  </div>
</nav>

<div class="pl-page">

<header class="pl-hero" id="top">
  <div class="pl-hero-inner">
    <p class="pl-kicker">Forecast · the customer economics · modeled, illustrative</p>
    <h1>One enterprise customer. {money(TPV)} of annual payment volume. Up to {money(Y1['Full'])} of revenue.</h1>
    <p class="pl-sub">VYB is building the financial operating layer for live commerce. This page takes one high-volume promoter's real, anonymized economics and shows how the money that flows through its business becomes VYB revenue at three depths of integration — <em>Base</em>, <em>Medium</em>, <em>Full</em> — and how that revenue expands, compounds, and scales across customers. Every figure is computed from the baseline and the assumptions at the end. None is a commitment.</p>
    <div class="pl-hero-actions">
      <a href="#expansion" class="pl-btn">Revenue expansion →</a>
      <a href="#scale" class="pl-btn-ghost">Platform scale</a>
      <a href="#assumptions" class="pl-btn-ghost">Assumptions &amp; risks</a>
    </div>
    <div class="kpis kpis-hero">
      {kpi(money(TPV), 'annual TPV · one customer', 'Total payment volume: what the customer pays artists, venues, vendors and crews in the modeled year.')}
      {kpi(money(Y1['Base']), 'Base · year one', f'{bps(take_bps["Base"])} · software only')}
      {kpi(money(Y1['Medium']), 'Medium · year one', f'{bps(take_bps["Medium"])} · software + payments + cards')}
      {kpi(money(Y1['Full']), 'Full · year one', f'{bps(take_bps["Full"])} · + financing')}
      {kpi(f'{take_bps["Base"]:.0f}–{take_bps["Full"]:.0f} bps', 'effective take rate', 'Revenue ÷ TPV, by integration depth.')}
      {kpi(money(per_1m['Full']), 'revenue per $1M of TPV', 'At Full. Medium: ' + money(per_1m['Medium']) + '.')}
      {kpi(money(fin_vol_y1), 'financing facilitated · year one', f'{fin_dates_y1:.0f} dates × {money(A["adv_per_date"])}; {money(fin_vol_rr)} at ten dates a year.')}
      {kpi(money(stream_y1['finance']), 'financing revenue · year one', 'Origination fee plus interest participation. VYB balance sheet deployed: $0.')}
    </div>
  </div>
</header>

<div class="pl-shell">
  <aside class="pl-rail">
    <div class="pl-rail-h">The case</div>
    <div id="plRail" class="pl-rail-nav">
      <a href="#customer"><span class="i">01</span> Customer economics</a>
      <a href="#expansion"><span class="i">02</span> Revenue expansion</a>
      <a href="#stack"><span class="i">03</span> Revenue stack</a>
      <a href="#unit"><span class="i">04</span> Unit economics</a>
      <a href="#scale"><span class="i">05</span> Platform scale</a>
      <a href="#flywheel"><span class="i">06</span> Capital flywheel</a>
      <a href="#capital"><span class="i">07</span> Capital efficiency</a>
      <a href="#mix"><span class="i">08</span> Revenue mix &amp; quality</a>
      <a href="#sensitivity"><span class="i">09</span> Sensitivity</a>
      <a href="#ramp"><span class="i">10</span> Ramp &amp; three years</a>
      <a href="#levels"><span class="i">11</span> The three levels</a>
      <a href="#date"><span class="i">12</span> One date, line by line</a>
      <a href="#customerside"><span class="i">13</span> The customer's side</a>
      <a href="#retention"><span class="i">14</span> Retention &amp; concentration</a>
      <a href="#assumptions"><span class="i">15</span> Assumptions &amp; risks</a>
    </div>
  </aside>

  <main class="pl-main">

    <section class="pl-sec" id="customer">
      <div class="pl-sec-num">01 — CUSTOMER ECONOMICS</div>
      <h2 class="pl-h">One enterprise customer → {money(TPV)} annual TPV → up to {money(Y1['Full'])} revenue.</h2>
      <p class="pl-lede">The customer is an independent live-entertainment promoter and producer headquartered in Las Vegas, operating nightclubs, theaters, arenas, festivals, residencies and a stadium run across a dozen North American markets. Its trailing eight months, show by show:</p>
      <div class="fc-stats" data-io="">
        <div><div class="n">{BASELINE['shows']}</div><div class="u">shows · Jan–Aug</div></div>
        <div><div class="n">{money(BASELINE['gross'])}</div><div class="u">gross revenue</div></div>
        <div><div class="n">{money(BASELINE['paid_out'])}</div><div class="u">paid out to counterparties</div></div>
        <div><div class="n">{money(BASELINE['profit'])}</div><div class="u">net profit · {pct(BASELINE['profit']/BASELINE['gross'])} margin</div></div>
        <div><div class="n">{BASELINE['attendance']/1e3:.0f}K</div><div class="u">attendance</div></div>
      </div>
      <div class="fc-table-wrap" data-io=""><table class="fc-table"><thead><tr><th>Tier</th><th>Shows</th><th>Avg gross</th><th>Avg paid out</th><th>Avg attendance</th><th>Margin</th></tr></thead><tbody>{tiers_html}</tbody></table></div>
      <div class="fc-two" style="margin-top:26px;" data-io="">
        <div>
          <div class="pl-sub-h">The modeled year · TPV</div>
          <table class="fc-table"><thead><tr><th>Case</th><th>Shows</th><th>Stadium dates</th><th>TPV</th><th>Gross</th></tr></thead><tbody>
            <tr><td>Low</td><td>{CASES['Low']['shows']}</td><td>{CASES['Low']['stadium_dates']}</td><td>{money(CASES['Low']['paid'])}</td><td>{money(CASES['Low']['gross'])}</td></tr>
            <tr class="hi"><td>Base</td><td>{B['shows']}</td><td>{B['stadium_dates']}</td><td>{money(TPV)}</td><td>{money(B['gross'])}</td></tr>
            <tr><td>High</td><td>{CASES['High']['shows']}</td><td>{CASES['High']['stadium_dates']}</td><td>{money(CASES['High']['paid'])}</td><td>{money(CASES['High']['gross'])}</td></tr>
          </tbody></table>
        </div>
        <div>
          <div class="pl-sub-h">Why TPV is the driver</div>
          <p class="pl-lede" style="font-size:15px;">VYB monetizes the money that moves, not seats or logins. TPV here is paid-out volume — the customer's payments to artists, venues, vendors and crews — because that is what VYB orchestrates and settles. Base is the current year's shape: the operating rhythm of {B['shows'] - B['stadium_dates']} theater, club and arena shows plus {B['stadium_dates']} stadium dates at the confirmed {money(sr['budget'], 2)} per-date budget. Seven of those dates are confirmed for the back half of this year, financed show-by-show at a {pct(sr['return'])} fixed return.</p>
        </div>
      </div>
      <p class="pl-note">Figures are the customer's own, lightly rounded; company and artists deliberately unnamed. The prior full year grossed {money(BASELINE['prior_year']['gross'])} with {money(BASELINE['prior_year']['profit'])} of profit; the current year passed that by spring. {BASELINE['pipeline']['on_sale']} further shows are on sale and {BASELINE['pipeline']['pending']} are pending.</p>
    </section>

    <section class="pl-sec" id="expansion">
      <div class="pl-sec-num">02 — REVENUE EXPANSION</div>
      <h2 class="pl-h">Revenue expands as VYB moves deeper into the customer's business.</h2>
      <p class="pl-lede">Same customer, same twelve months, same TPV. What changes is how much of the customer's financial flow runs through VYB — and each layer VYB takes on carries its own economics.</p>
      <div class="fc-expand" data-io="">
        <div class="ex"><div class="t" style="color:{S1}">Base</div><div class="n">{money(Y1['Base'])}</div><div class="m">1×</div><div class="bar"><i style="width:{Y1['Base']/Y1['Full']*100:.1f}%;background:{S1}"></i></div><div class="d">Event financial control center. Reads ticketing, bank, accounting and contracts into one ledger. Moves nothing.</div></div>
        <div class="ex"><div class="t" style="color:{S2}">Medium</div><div class="n">{money(Y1['Medium'])}</div><div class="m">{mx(mult['bm'])}</div><div class="bar"><i style="width:{Y1['Medium']/Y1['Full']*100:.1f}%;background:{S2}"></i></div><div class="d">Payment orchestration on the customer's own rails and virtual cards, under its approval policy. {pct(A['routed_q']['Medium'][3])} of TPV routed by Q4.</div></div>
        <div class="ex hi"><div class="t" style="color:{S3}">Full</div><div class="n">{money(Y1['Full'])}</div><div class="m">{mx(mult['bf'])}</div><div class="bar"><i style="width:100%;background:{S3}"></i></div><div class="d">Agents execute inside the policy; VYB originates working capital against contracted receivables. {pct(A['routed_q']['Full'][3])} routed by Q4; {mx(mult['mf'])} Medium.</div></div>
      </div>
      <div class="fc-callout" data-io=""><div class="fc-callout-h">The investor takeaway</div><p>VYB can expand revenue <b>{mx(mult['bf'])}</b> inside an existing enterprise relationship without acquiring another customer — by moving from software into payments, cards and financing. Revenue per customer, not customer count, is the first growth lever.</p></div>
    </section>

    <section class="pl-sec" id="stack">
      <div class="pl-sec-num">03 — REVENUE STACK</div>
      <h2 class="pl-h">Software → payments → cards → financing. Four layers on one customer.</h2>
      <p class="pl-lede">At Full integration, year one, the same {money(TPV)} of TPV is monetized four ways. VYB is not dependent on a single stream — and the streams that grow fastest are the transactional and financial ones.</p>
      <div class="fc-chain" data-io="">
        <div class="cn"><div class="k">Enterprise customer</div><div class="v">the promoter</div></div><div class="ar">↓</div>
        <div class="cn"><div class="k">Annual TPV</div><div class="v">{money(TPV)}</div></div><div class="ar">↓</div>
        <div class="cn wide">
          <div class="k">Monetization layers · Full · year one</div>
          <div class="layers">
            <div><i style="background:{S1}"></i><b>Software</b><span>{money(stream_y1['platform'] + stream_y1['impl'])}</span><small>platform {money(stream_y1['platform'])} + implementation {money(stream_y1['impl'])}</small></div>
            <div><i style="background:{S2}"></i><b>Payments</b><span>{money(stream_y1['payments'])}</span><small>{A['take']*100:.2f}% on {money(routed_y1['Full'])} routed</small></div>
            <div><i style="background:{S5}"></i><b>Cards</b><span>{money(stream_y1['cards'])}</span><small>interchange share on virtual-card spend</small></div>
            <div><i style="background:{S3}"></i><b>Financing</b><span>{money(stream_y1['finance'])}</span><small>origination + interest participation on {money(fin_vol_y1)} facilitated</small></div>
          </div>
        </div><div class="ar">↓</div>
        <div class="cn hi"><div class="k">Full integration · VYB revenue</div><div class="v">{money(Y1['Full'])}</div></div>
      </div>
      <div class="fc-chart-wrap" data-io="">{STACK}</div>
    </section>

    <section class="pl-sec" id="unit">
      <div class="pl-sec-num">04 — UNIT ECONOMICS</div>
      <h2 class="pl-h">TPV → take rate → revenue → gross profit.</h2>
      <p class="pl-lede">Modeled gross margins by stream. Payments carry rail and network cost; implementation is services; financing is high-margin to VYB because the capital partner carries the funding cost and VYB earns fees and a share of interest.</p>
      <div class="kpis" data-io="">
        {kpi(money(TPV), 'TPV')}
        {kpi(bps(take_bps['Full']), 'effective take rate · Full')}
        {kpi(money(Y1['Full']), 'revenue · Full · year one')}
        {kpi(money(gp_full), f'gross profit · {pct(gp_full/Y1["Full"])} margin')}
      </div>
      <div class="fc-table-wrap" data-io=""><table class="fc-table"><thead><tr><th>Stream · Full · year one</th><th>Revenue</th><th>Gross margin</th><th>Gross profit</th><th>Cost basis</th></tr></thead><tbody>{unit_rows}<tr class="tot"><td>Total</td><td>{money(Y1['Full'])}</td><td>{pct(gp_full/Y1['Full'])}</td><td>{money(gp_full)}</td><td></td></tr></tbody></table></div>
      <div class="fc-table-wrap" data-io=""><table class="fc-table"><thead><tr><th>By level · year one</th><th>Revenue</th><th>Take rate</th><th>Revenue per $1M TPV</th><th>Gross profit</th></tr></thead><tbody>
        {''.join(f'<tr{" class=hi" if lvl=="Full" else ""}><td>{lvl}</td><td>{money(Y1[lvl])}</td><td>{bps(take_bps[lvl])}</td><td>{money(per_1m[lvl])}</td><td>{money(gp_level[lvl])}</td></tr>' for lvl in LEVELS)}
      </tbody></table></div>
      <p class="pl-note">Not yet modeled, to be added as operating data arrives: contribution margin after support and risk reserves, customer acquisition cost, and CAC payback. At these revenue levels a single enterprise sale repays a substantial acquisition cost inside year one.</p>
    </section>

    <section class="pl-sec" id="scale">
      <div class="pl-sec-num">05 — PLATFORM SCALE</div>
      <h2 class="pl-h">A small number of high-volume customers is a large financial platform.</h2>
      <p class="pl-lede">An illustrative scaling scenario, not a company forecast: additional enterprise customers with economics like this one, each at Base volume. VYB does not need millions of consumers; it needs dozens of operators who move a lot of money.</p>
      <div class="fc-scale" data-io="">
        <label for="scaleN">Enterprise customers <b id="scaleNv">1</b></label>
        <input type="range" id="scaleN" min="1" max="100" value="1" step="1">
        <div class="kpis">
          {kpi(money(TPV), 'annual TPV', '').replace('class="n"', 'class="n" id="sTPV"')}
          {kpi(money(Y1['Medium']), 'Medium · year one', '').replace('class="n"', 'class="n" id="sMed"')}
          {kpi(money(Y1['Full']), 'Full · year one', '').replace('class="n"', 'class="n" id="sFull"')}
          {kpi(money(Y3['Full']), 'Full · year three', '').replace('class="n"', 'class="n" id="sFull3"')}
        </div>
      </div>
      <div class="fc-table-wrap" data-io=""><table class="fc-table"><thead><tr><th>Customers</th><th>Annual TPV</th><th>Medium · year one</th><th>Full · year one</th><th>Full · year three</th></tr></thead><tbody>{scale_rows}</tbody></table></div>
      <p class="pl-note">100 customers × {money(TPV)} TPV ≈ {money(100*TPV)} of annual payment volume. Illustrative: assumes each customer resembles this one, and ignores the network revenue that would arise when their counterparties transact with each other on VYB.</p>
    </section>

    <section class="pl-sec" id="flywheel">
      <div class="pl-sec-num">06 — CAPITAL FLYWHEEL</div>
      <h2 class="pl-h">Transactions → data → underwriting → financing → more transactions.</h2>
      <p class="pl-lede">This is the layer that separates VYB from a payments company. Every settled show adds settlement timing, vendor reliability and real room economics to a record no one else has — and that record underwrites the next advance, which funds the next show, which routes more money through VYB.</p>
      <div class="fc-fly-wrap" data-io="">{FLY}</div>
    </section>

    <section class="pl-sec" id="capital">
      <div class="pl-sec-num">07 — CAPITAL EFFICIENCY</div>
      <h2 class="pl-h">Capital facilitated, not capital deployed.</h2>
      <p class="pl-lede">The financing opportunity is not balance-sheet intensive for VYB. A capital partner funds each advance; VYB originates it against contracted box-office receivables, services it through the ledger, and is repaid automatically from settlement before other distributions.</p>
      <div class="kpis" data-io="">
        {kpi(money(fin_vol_y1), 'capital facilitated · year one', f'{fin_dates_y1:.0f} dates')}
        {kpi(money(fin_vol_rr), 'capital facilitated · run-rate', '10 dates a year')}
        {kpi('$0', 'VYB balance sheet deployed', 'the capital partner funds; VYB originates')}
        {kpi(money(stream_y1['finance']), 'financing revenue · year one', money(vyb_per_date) + ' per date')}
      </div>
      <div class="fc-two" data-io="">
        <div>
          <div class="pl-sub-h">One date, made explicit</div>
          {kv([('Advance', f"{money(A['adv_per_date'])} against contracted receivables"), ('Term', f"{A['adv_days']} days, repaid from settlement"), ('Rate', f"{pct(A['adv_apr'])} APR"), ('Interest for the term', f"{money(A['adv_per_date'])} × {pct(A['adv_apr'])} × {A['adv_days']}/365 = {money(interest_per_date)}"), ('Origination fee', f"{pct(A['orig_fee'])} = {money(A['adv_per_date']*A['orig_fee'])}"), ('VYB keeps', f"origination {money(A['adv_per_date']*A['orig_fee'])} + {pct(A['spread_share'])} of interest {money(interest_per_date*A['spread_share'])} = {money(vyb_per_date)}"), ('Capital partner keeps', f"{pct(1-A['spread_share'])} of interest = {money(interest_per_date*(1-A['spread_share']))}"), ('Customer cost, VYB', money(interest_per_date + A['adv_per_date']*A['orig_fee'])), ('Customer cost today', f"{pct(sr['return'])} fixed on {money(A['adv_per_date'])} = {money(today_per_date)}"), ('Customer saves', f"{money(today_per_date - (interest_per_date + A['adv_per_date']*A['orig_fee']))} per date")])}
        </div>
        <div>
          <div class="pl-sub-h">VYB's role</div>
          <ul class="fc-list">
            <li><b>Originator.</b> Underwrites against the ledger's settlement history; sizes the advance to production and venue deposits, never the artist guarantee.</li>
            <li><b>Servicer.</b> Repayment is a ledger event: box-office settlement clears the advance first, automatically.</li>
            <li><b>Fee and participation.</b> A {pct(A['orig_fee'])} origination fee and {pct(A['spread_share'])} of interest; no funding cost, no principal at risk on VYB's balance sheet.</li>
            <li><b>Not a lender.</b> The capital partner is the lender of record; VYB does not use its own balance sheet in this model.</li>
          </ul>
          <p class="pl-note">The customer's current instrument is a {pct(sr['return'])} fixed return per date on a {money(sr['budget'], 2)} unit, repaid from proceeds within months. We compare the cost of the two structures for the same {money(A['adv_per_date'])} over the same term rather than annualizing either, since a short-duration fixed return is not a yield.</p>
        </div>
      </div>
    </section>

    <section class="pl-sec" id="mix">
      <div class="pl-sec-num">08 — REVENUE MIX &amp; QUALITY</div>
      <h2 class="pl-h">From software revenue to transactional and financial revenue.</h2>
      <div class="fc-two" data-io="">
        <div class="fc-donut-wrap">{DONUT}{legend([(n, STREAM_COL[k]) for n, k in STREAMS])}</div>
        <div>
          <div class="pl-sub-h">Full · year one</div>
          <table class="fc-table"><thead><tr><th>Stream</th><th>Revenue</th><th>Share</th><th>Character</th></tr></thead><tbody>
            {''.join(f'<tr><td>{n}</td><td>{money(stream_y1[k])}</td><td>{pct(stream_y1[k]/Y1["Full"])}</td><td class="m">{ch}</td></tr>' for (n, k), ch in zip(STREAMS, ['recurring, contractual', 'one-time services', 'usage-based', 'usage-based', 'financial']))}
          </tbody></table>
        </div>
      </div>
      <div class="fc-quality" data-io="">
        <div class="q"><div class="t">Recurring · contractual</div><div class="n">{money(stream_y1['platform'])}</div><div class="d">Platform fees and enterprise software. Predictable; the floor of the relationship.</div></div>
        <div class="q"><div class="t">Usage-based</div><div class="n">{money(stream_y1['payments'] + stream_y1['cards'])}</div><div class="d">Payment orchestration and card spend. Scales with TPV and with routed share; retained as long as money moves.</div></div>
        <div class="q"><div class="t">Financial</div><div class="n">{money(stream_y1['finance'])}</div><div class="d">Origination and interest participation. The upside layer; scales with the stadium calendar and with underwriting confidence.</div></div>
      </div>
    </section>

    <section class="pl-sec" id="sensitivity">
      <div class="pl-sec-num">09 — SENSITIVITY</div>
      <h2 class="pl-h">Volume × integration depth, year one.</h2>
      <p class="pl-lede">Base is a software fee and does not move with volume. Medium scales with the money that moves. Full scales with the money and with the stadium calendar, because that is where the financing lives.</p>
      <div data-io="">{HEAT}</div>
      <p class="pl-note">Cell shading is proportional to revenue; the small figure is the effective take rate on that case's TPV.</p>
    </section>

    <section class="pl-sec" id="ramp">
      <div class="pl-sec-num">10 — RAMP &amp; THREE YEARS</div>
      <h2 class="pl-h">Revenue follows adoption, then the stadium calendar.</h2>
      <p class="pl-lede">Year one by quarter at Base volume: Base is flat after the implementation quarter; Medium climbs with routed share; Full steps up in the third quarter, when financing starts against the settlement history the ledger has by then earned.</p>
      <div class="fc-chart-wrap" data-io="">{legend([(l, SERIES[l]) for l in LEVELS])}{LINE_SVG}<div class="fc-tip" id="fcTip" hidden></div></div>
      <p class="pl-lede" style="margin-top:34px;">Three years, volume held flat at Base to isolate adoption. Routed share settles at {pct(A['routed_y']['Medium'][2])} (Medium) and {pct(A['routed_y']['Full'][2])} (Full); financed dates at {pct(A['fin_dates_y'][2])} of the run.</p>
      <div class="fc-chart-wrap" data-io="">{legend([(l, SERIES[l]) for l in LEVELS])}{BAR_SVG}</div>
      <div class="fc-table-wrap" data-io=""><table class="fc-table"><thead><tr><th>VYB revenue</th><th>Year one</th><th>Year two</th><th>Year three</th></tr></thead><tbody>{''.join(f'<tr{" class=hi" if lvl=="Full" else ""}><td>{lvl}</td><td>{money(Y1[lvl])}</td><td>{money(Y2[lvl])}</td><td>{money(Y3[lvl])}</td></tr>' for lvl in LEVELS)}</tbody></table></div>
    </section>

    <section class="pl-sec" id="levels">
      <div class="pl-sec-num">11 — THE THREE LEVELS</div>
      <h2 class="pl-h">What each level is, and what it earns by quarter.</h2>
      <p class="pl-lede">Each level contains the one before it. The customer can stop at any of them.</p>
      <div class="fc-flow-wrap" data-io="">{FLOW}</div>
      <div class="fc-level-block" data-io=""><div class="lh" style="color:{S1}">Base — event financial control center</div><div class="fc-two">{'<div>' + qtable('Base') + '</div>'}<div>{kv([('What it is', 'Every event a financial object: counterparties, obligations, invoices, approvals, settlement status, live margin. Reads the customer’s systems; moves nothing.'), ('Pricing', f"{money(A['impl'])} implementation + {money(A['platform_base']/12)} / month"), ('Year two', money(Y2['Base']))])}</div></div></div>
      <div class="fc-level-block" data-io=""><div class="lh" style="color:{S2}">Medium — payment orchestration</div><div class="fc-two">{'<div>' + qtable('Medium') + '</div>'}<div>{kv([('What it is', 'Vendor, crew, production, marketing and artist payments execute through VYB on the customer’s existing bank rails and virtual cards, under its approval policy. Reconciled at execution.'), ('Routed share', ' → '.join(pct(x) for x in A['routed_q']['Medium']) + ' by quarter'), ('Take', f"{A['take']*100:.2f}% blended + {pct(A['card_share'])} of card spend"), ('Year two', money(Y2['Medium']))])}</div></div></div>
      <div class="fc-level-block" data-io=""><div class="lh" style="color:{S3}">Full — intelligent operator with embedded finance</div><div class="fc-two">{'<div>' + qtable('Full') + '</div>'}<div>{kv([('What it is', 'Agents run approvals and settlement inside the policy; VYB originates advances against contracted receivables with a capital partner.'), ('Routed share', ' → '.join(pct(x) for x in A['routed_q']['Full']) + ' by quarter'), ('Financed dates', f"none in H1, {pct(A['fin_dates_q'][2])} of the year’s dates in Q3, {pct(A['fin_dates_q'][3])} in Q4"), ('Year two', money(Y2['Full']))])}</div></div></div>
    </section>

    <section class="pl-sec" id="date">
      <div class="pl-sec-num">12 — ONE DATE, LINE BY LINE</div>
      <h2 class="pl-h">The stadium date through each level.</h2>
      <p class="pl-lede">The confirmed per-date budget of {money(sr['budget'], 2)}. Base makes every line a tracked obligation. Medium moves it on a rail under the customer's policy. Full finances the production and venue slice — {money(sr['production'] + sr['venue'], 2)} of the {money(sr['budget'], 2)} — and lets agents execute inside the caps.</p>
      <div class="fc-table-wrap" data-io=""><table class="fc-table" style="font-size:13.5px;"><thead><tr><th>Line</th><th>Per date</th><th>Base</th><th>Medium</th><th>Full adds</th></tr></thead><tbody>{date_rows_html}</tbody></table></div>
      <div class="fc-callout" data-io=""><div class="fc-callout-h">The approval policy behind every payment</div><p>Set by the customer on day one and enforced by the system: recurring payees within budget and under <b>$10,000</b> execute and report; <b>$10,000–$100,000</b>, new payees and change orders are prepared for one confirmation by the finance lead; anything over <b>$100,000</b>, and every talent or venue settlement, needs two signatures in order. Out-of-policy items are blocked until resolved. The rails underneath — bank wire and ACH, virtual cards with per-persona caps, a stablecoin rail for the cross-border crew presented as dollars, machine payments for data — are chosen by the router per payment; the customer sees a balance, approvals and settlement, never a network name.</p></div>
    </section>

    <section class="pl-sec" id="customerside">
      <div class="pl-sec-num">13 — THE CUSTOMER'S SIDE</div>
      <h2 class="pl-h">At every level the customer keeps more than VYB earns.</h2>
      <div class="fc-table-wrap" data-io=""><table class="fc-table"><thead><tr><th>Year one · Base volume</th><th>Base</th><th>Medium</th><th>Full</th></tr></thead><tbody>
        <tr><td>Finance hours saved</td>{''.join(f"<td>{money(V[l]['hours_value'])}</td>" for l in LEVELS)}</tr>
        <tr><td>Leakage caught</td>{''.join(f"<td>{money(V[l]['leak']) if V[l]['leak'] else '—'}</td>" for l in LEVELS)}</tr>
        <tr><td>Cost of capital saved</td>{''.join(f"<td>{money(V[l]['capital']) if V[l]['capital'] else '—'}</td>" for l in LEVELS)}</tr>
        <tr class="tot"><td>Customer value</td>{''.join(f"<td>{money(V[l]['total'])}</td>" for l in LEVELS)}</tr>
        <tr><td>VYB revenue</td>{''.join(f"<td>{money(Y1[l])}</td>" for l in LEVELS)}</tr>
        <tr><td>Value per VYB dollar</td>{''.join(f"<td>{V[l]['total']/Y1[l]:.1f}×</td>" for l in LEVELS)}</tr>
      </tbody></table></div>
      <p class="pl-note">Not counted: settlement moving from weeks to the night of the show, vendor inquiries falling to near zero, margin known before doors, one ledger instead of six systems. The value ratio is why the integration deepens: each level pays for itself on the customer's side before VYB's revenue grows.</p>
    </section>

    <section class="pl-sec" id="retention">
      <div class="pl-sec-num">14 — RETENTION &amp; CONCENTRATION</div>
      <h2 class="pl-h">The metrics this page will carry once customers are live.</h2>
      <p class="pl-lede">For a platform that monetizes volume, <b>TPV retention</b> matters as much as logo retention: a customer's value can multiply while the customer count stays flat. These frames are deliberately empty until there is data to put in them.</p>
      <div class="fc-two" data-io="">
        <div><div class="pl-sub-h">Expansion &amp; retention</div>{kv([('Gross revenue retention', '—'), ('Net revenue retention', '—'), ('Logo retention', '—'), ('TPV retention', '—'), ('Expansion revenue', '—'), ('Revenue per customer', f'{money(Y1["Full"])} modeled at Full'), ('Average TPV per customer', f'{money(TPV)} modeled')])}</div>
        <div><div class="pl-sub-h">Concentration</div>{kv([('Top 1 customer · % of revenue', '100% in this model — one customer'), ('Top 5 customers', '—'), ('Top 10 customers', '—')])}<p class="pl-note">Concentration is the honest risk of an enterprise-led model and is presented as such. The scale scenario in section 05 shows how it dilutes.</p></div>
      </div>
    </section>

    <section class="pl-sec" id="assumptions">
      <div class="pl-sec-num">15 — ASSUMPTIONS &amp; RISKS</div>
      <h2 class="pl-h">Every number above traces to one of these.</h2>
      <div class="pl-rows">
        <div class="pl-row" data-io=""><div class="r-i">01</div><div class="r-t">Pricing</div><div class="r-d">Implementation {money(A['impl'])} one-time. Platform {money(A['platform_base']/12)} / month at Base and Medium, {money(A['platform_full']/12)} / month at Full for the agent and intelligence layer. Payments {A['take']*100:.2f}% blended on orchestrated volume. Cards: VYB keeps {pct(A['card_share'])} of spend as its interchange share, on {pct(A['card_frac']['Medium'])}–{pct(A['card_frac']['Full'])} of TPV moving to virtual cards. Within the ranges on the VYB pitch.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">02</div><div class="r-t">Adoption</div><div class="r-d">Routed share of TPV by quarter: Medium {' → '.join(pct(x) for x in A['routed_q']['Medium'])}; Full {' → '.join(pct(x) for x in A['routed_q']['Full'])}. Years two and three: Medium {pct(A['routed_y']['Medium'][1])}, {pct(A['routed_y']['Medium'][2])}; Full {pct(A['routed_y']['Full'][1])}, {pct(A['routed_y']['Full'][2])}. Artist guarantees move last.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">03</div><div class="r-t">Financing</div><div class="r-d">{money(A['adv_per_date'])} per stadium date against contracted receivables for {A['adv_days']} days at {pct(A['adv_apr'])} APR, funded by a capital partner; VYB earns a {pct(A['orig_fee'])} origination fee and {pct(A['spread_share'])} of interest. Financed dates: none in H1, {pct(A['fin_dates_q'][2])} of the year's dates in Q3, {pct(A['fin_dates_q'][3])} in Q4; {pct(A['fin_dates_y'][1])} and {pct(A['fin_dates_y'][2])} in years two and three. Compared against the customer's current {pct(sr['return'])} fixed return per date over the same term.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">04</div><div class="r-t">Gross margin</div><div class="r-d">Platform {pct(GM['platform'])}, implementation {pct(GM['impl'])}, payments {pct(GM['payments'])} (rail and network costs ≈ 0.12% of routed volume), cards {pct(GM['cards'])}, financing {pct(GM['finance'])} (servicing only; funding cost with the partner). Modeled, not measured.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">05</div><div class="r-t">Customer value</div><div class="r-d">Finance hours per show today — stadium {A['hours']['Stadium']}, arena {A['hours']['Arena / large room']}, theater or club {A['hours']['Theater / club']}, small room {A['hours']['Small room / activation']} — at {money(A['hour_cost'])} loaded; {pct(A['hours_saved']['Base'])} / {pct(A['hours_saved']['Medium'])} / {pct(A['hours_saved']['Full'])} saved by level. Leakage {A['leak']*100:.2f}% of routed volume.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">06</div><div class="r-t">Volume</div><div class="r-d">Non-stadium activity annualized from the trailing eight months ({money(non_stadium_paid_annual)} across {non_stadium_shows_annual} shows); stadium dates at the confirmed {money(sr['budget'], 2)} per-date budget; gross at the trailing {pct(0.686)} paid-out-to-gross ratio. Held flat across the three-year view and the scale scenario.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">07</div><div class="r-t">Risks</div><div class="r-d"><b>Adoption:</b> routed share depends on the customer moving payment categories onto VYB; artist guarantees may never move. <b>Financing partner:</b> the Full case needs a capital partner on acceptable terms and underwriting that the ledger must earn. <b>Concentration:</b> one customer is 100% of this model. <b>Stadium calendar:</b> financing revenue is tied to a handful of dates a year. <b>Regulatory:</b> routed volume at these levels carries VYB into payment-facilitator registration, with its own timeline and cost. <b>Confidentiality:</b> the baseline is one company's real figures, anonymized.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">08</div><div class="r-t">What this is not</div><div class="r-d">Not an offer, a quote, a company forecast or a guarantee. Pricing, adoption and financing terms are a conversation; this page is the shape of one.</div></div>
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
    <div><div class="footer-brand"><span class="app-icon">v</span> vyb</div><div class="footer-meta">© 2026 VYB · FORECAST · MODELED, ILLUSTRATIVE</div></div>
    <div class="footer-links"><a href="/">Home</a><a href="/#enterprise">Enterprise</a><a href="/pulse">VYB Pulse</a><a href="mailto:blake@vybapp.io?subject=VYB%20forecast">Contact</a></div>
  </div>
</footer>
"""

extra_js = """
(function(){
  function fmt(v){return v>=1e9?'$'+(v/1e9).toFixed(1)+'B':v>=1e6?'$'+(v/1e6).toFixed(1)+'M':'$'+Math.round(v/1e3)+'K';}
  var tip=document.getElementById('fcTip'), svg=document.querySelector('svg[data-chart=line]');
  if(tip&&svg){ var D=__TIP__; var xh=svg.querySelector('.xh');
    svg.querySelectorAll('.hit').forEach(function(r){
      r.addEventListener('mouseenter',function(){var i=+r.dataset.i; xh.setAttribute('x1',D.x[i]); xh.setAttribute('x2',D.x[i]); xh.setAttribute('visibility','visible');
        tip.innerHTML='<b>'+D.q[i]+'</b>'+Object.keys(D.series).map(function(k){return '<span>'+k+' <em>'+fmt(D.series[k][i])+'</em></span>';}).join(''); tip.hidden=false;
        var b=svg.getBoundingClientRect(), w=svg.parentNode.getBoundingClientRect(); var px=(D.x[i]/760)*b.width+(b.left-w.left); tip.style.left=Math.min(px,w.width-190)+'px';});
      r.addEventListener('mouseleave',function(){tip.hidden=true; xh.setAttribute('visibility','hidden');});
    }); }
  document.querySelectorAll('svg[data-chart=bar] .bar').forEach(function(b){ var t=document.createElementNS('http://www.w3.org/2000/svg','title'); t.textContent=b.dataset.l+' \\u00b7 '+b.dataset.y+' \\u00b7 '+fmt(+b.dataset.v); b.appendChild(t); });
  var s=document.getElementById('scaleN'); if(s){ var U={tpv:__TPV__, med:__MED__, full:__FULL__, full3:__FULL3__};
    var upd=function(){ var n=+s.value; document.getElementById('scaleNv').textContent=n; document.getElementById('sTPV').textContent=fmt(n*U.tpv); document.getElementById('sMed').textContent=fmt(n*U.med); document.getElementById('sFull').textContent=fmt(n*U.full); document.getElementById('sFull3').textContent=fmt(n*U.full3); };
    s.addEventListener('input',upd); upd(); }
})();
""".replace('__TIP__', LINE_TIP).replace('__TPV__', str(round(TPV))).replace('__MED__', str(round(Y1['Medium']))).replace('__FULL__', str(round(Y1['Full']))).replace('__FULL3__', str(round(Y3['Full'])))

TITLE = "VYB — Forecast"
DESC = "The customer economics of VYB: one enterprise promoter's real, anonymized payment volume becomes revenue at three integration depths — and how that revenue expands, compounds and scales."
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
{extra_js}
</script>
</body></html>
"""
open(OUT, 'w', encoding='utf-8').write(page)
print(f"wrote {OUT} ({len(page)} bytes)")
print('take bps', {k: round(v, 1) for k, v in take_bps.items()}, '| mult', {k: round(v, 2) for k, v in mult.items()}, '| streams', {k: money(v) for k, v in stream_y1.items()}, '| GP full', money(gp_full), pct(gp_full / Y1['Full']))
