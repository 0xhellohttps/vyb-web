#!/usr/bin/env python3
"""Assemble /Users/b/Projects/vyb-web/raise.html — VYB capital strategy:
$5M seed → commercial validation → product-market fit → $100M+ Series A.
Reuses site.css + pulse_extra.css + forecast_extra.css (+ raise_extra.css).
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/Users/b/Projects/vyb-web/raise.html'

SEED = 5e6; PRE = 25e6; POST = PRE + SEED; OWN = SEED / POST
USE = [('Product & engineering', 1.5e6), ('Payments, compliance & infrastructure', .75e6), ('Enterprise GTM & deployment', .75e6),
       ('Strategic commercial deployment & market validation', .75e6), ('Key hires', .5e6), ('Legal, security & operations', .25e6), ('Reserve / working capital', .5e6)]
SERIES_A = [('Payments infrastructure & financial rails', 25e6), ('Enterprise sales & implementation', 20e6), ('Financial products, cards & financing', 15e6),
            ('AI / agentic financial infrastructure', 15e6), ('Geographic expansion', 10e6), ('Strategic acquisitions / technology', 10e6), ('Corporate reserve', 5e6)]
TPV1 = 142.1e6; REV = {'Base': 55e3, 'Medium': 333e3, 'Full': 963e3}
SCALE = [10, 25, 50, 100]

def money(x):
    if x >= 1e9: return f'${x/1e9:.1f}B'
    if x >= 1e6: return f'${x/1e6:.2f}M'.replace('.00M', 'M').replace('.50M', '.5M')
    return f'${x/1e3:.0f}K'
def pct(x): return f'{x*100:.1f}%'

COLS = ['var(--s1)', 'var(--s2)', 'var(--s3)', 'var(--s4)', 'var(--s5)', 'var(--s6)', 'var(--s7)']

def stack(items, title_id, title):
    total = sum(v for _, v in items); W = 760
    s = [f'<svg class="fc-stack" viewBox="0 0 {W} 44" role="img" aria-labelledby="{title_id}"><title id="{title_id}">{title}</title>']
    x = 0
    for i, (n, v) in enumerate(items):
        w = W * v / total
        s.append(f'<rect x="{x+1:.1f}" y="8" width="{max(w-2,0):.1f}" height="28" rx="4" fill="{COLS[i]}"><title>{n} · {money(v)}</title></rect>'); x += w
    s.append('</svg>')
    return '\n'.join(s)

def legend(items):
    return '<div class="fc-legend">' + ''.join(f'<span><i style="background:{COLS[i]}"></i>{n} · {money(v)}</span>' for i, (n, v) in enumerate(items)) + '</div>'

def table(items, head):
    total = sum(v for _, v in items)
    rows = ''.join(f'<tr><td>{n}</td><td>{money(v)}</td><td>{v/total*100:.0f}%</td></tr>' for n, v in items)
    return f'<table class="fc-table"><thead><tr><th>{head}</th><th>Allocation</th><th>Share</th></tr></thead><tbody>{rows}<tr class="tot"><td>Total</td><td>{money(total)}</td><td>100%</td></tr></tbody></table>'

def kpi(n, u, l=''):
    return f'<div class="kpi"><div class="n">{n}</div><div class="u">{u}</div>{f"<div class=l>{l}</div>" if l else ""}</div>'
def kv(rows):
    return '<div class="fc-kv">' + ''.join(f'<div class="fc-kv-row"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in rows) + '</div>'
def chips(items):
    return '<div class="pl-chips">' + ''.join(f'<span class="pl-chip">{i}</span>' for i in items) + '</div>'

def stage(n, name, role, lede, validates, achieved, col):
    return f'''<div class="rs-stage" data-io="">
      <div class="rs-num" style="color:{col}">Stage {n} · {role}</div>
      <h3>{name}</h3>
      <p>{lede}</p>
      <div class="pl-sub-h" style="margin-top:16px;">Validates</div>{chips(validates)}
      <div class="rs-ach"><b>Validation achieved:</b> {achieved}</div>
    </div>'''

css = open(os.path.join(HERE, 'site.css')).read()
extra = open(os.path.join(HERE, 'pulse_extra.css')).read() + open(os.path.join(HERE, 'forecast_extra.css')).read() + open(os.path.join(HERE, 'raise_extra.css')).read()
js = open(os.path.join(HERE, 'build_pulse.py')).read().split('js = """')[1].split('"""')[0]

body = f"""<nav>
  <a href="/" class="nav-logo"><span class="app-icon">v</span> vyb</a>
  <div class="nav-right">
    <a href="/#features" class="nav-link">Features</a>
    <a href="/#enterprise" class="nav-link">Enterprise</a>
    <a href="/forecast" class="nav-link">Forecast</a>
    <a href="/pulse" class="nav-link">VYB Pulse</a>
    <a href="mailto:blake@vybapp.io?subject=VYB%20seed" class="nav-buy-btn">Talk to us</a>
    <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode"><span class="tt-icon tt-sun">☀️</span><span class="tt-icon tt-moon">🌙</span></button>
  </div>
</nav>

<div class="pl-page">

<header class="pl-hero" id="top">
  <div class="pl-hero-inner">
    <p class="pl-kicker">Capital strategy · seed</p>
    <h1>{money(SEED)} to prove it. $100M+ to scale it.</h1>
    <p class="pl-sub">VYB is building the financial operating system for live commerce — the financial workflows of artists, management, promoters, venues, vendors and event operators on one ledger. The financing strategy is a deliberate progression: a <em>{money(SEED)} seed</em> funds production infrastructure and three strategic commercial deployments that turn a forecast into proof, so that the next round is an <em>institutional Series A</em> for scaling a financial network that already exists.</p>
    <div class="pl-hero-actions">
      <a href="#validation" class="pl-btn">The validation strategy →</a>
      <a href="#seed" class="pl-btn-ghost">The seed</a>
      <a href="#seriesa" class="pl-btn-ghost">The Series A</a>
    </div>
    <div class="kpis kpis-hero">
      {kpi(money(SEED), 'seed · target raise', 'Build production infrastructure, deploy commercially, generate TPV and recurring revenue.')}
      {kpi(money(PRE) + ' → ' + money(POST), 'pre → post-money · target', f'≈ {pct(OWN)} to new investors before other capitalization considerations.')}
      {kpi('3', 'strategic deployments', 'Promoter → artist management → institutional venue.')}
      {kpi('$100M+', 'Series A · strategic target', '$75M–$125M+, sized to the metrics VYB has generated by then.')}
    </div>
  </div>
</header>

<div class="pl-shell">
  <aside class="pl-rail">
    <div class="pl-rail-h">The plan</div>
    <div id="plRail" class="pl-rail-nav">
      <a href="#thesis"><span class="i">01</span> The progression</a>
      <a href="#validation"><span class="i">02</span> Customer validation</a>
      <a href="#sequence"><span class="i">03</span> Why the sequence</a>
      <a href="#seed"><span class="i">04</span> The {money(SEED)} seed</a>
      <a href="#proceeds"><span class="i">05</span> Use of proceeds</a>
      <a href="#mission"><span class="i">06</span> Forecast → proof</a>
      <a href="#economics"><span class="i">07</span> The economic model</a>
      <a href="#network"><span class="i">08</span> Network economics</a>
      <a href="#seriesa"><span class="i">09</span> The Series A</a>
      <a href="#narrative"><span class="i">10</span> The narrative</a>
      <a href="#deploy"><span class="i">11</span> Series A deployment</a>
      <a href="#capital"><span class="i">12</span> Equity vs. financing capital</a>
      <a href="#roadmap"><span class="i">13</span> Capital roadmap</a>
      <a href="#captable"><span class="i">14</span> Cap table objective</a>
      <a href="#philosophy"><span class="i">15</span> Capital philosophy</a>
    </div>
  </aside>

  <main class="pl-main">

    <section class="pl-sec" id="thesis">
      <div class="pl-sec-num">01 — THE PROGRESSION</div>
      <h2 class="pl-h">Seed → commercial validation → product-market fit → institutional Series A.</h2>
      <p class="pl-lede">The seed is not runway. It is the capital that builds production infrastructure, executes strategic commercial deployments, generates meaningful transaction volume, establishes recurring revenue, and proves VYB can operate across multiple layers of the live-entertainment ecosystem.</p>
      <div class="fc-chain" data-io="">
        <div class="cn"><div class="k">Seed</div><div class="v">{money(SEED)}</div></div><div class="ar">↓</div>
        <div class="cn"><div class="k">Commercial validation</div><div class="v">three deployments</div></div><div class="ar">↓</div>
        <div class="cn"><div class="k">Product-market fit</div><div class="v">repeatability</div></div><div class="ar">↓</div>
        <div class="cn hi"><div class="k">Institutional Series A</div><div class="v">$100M+</div></div>
      </div>
    </section>

    <section class="pl-sec" id="validation">
      <div class="pl-sec-num">02 — CUSTOMER VALIDATION</div>
      <h2 class="pl-h">Three relationships. Three different things proven.</h2>
      <p class="pl-lede">The target customer progression is <b>IKON → Red Light Management → Mercedes-Benz Stadium</b>. Each is a different validation point, not a logo.</p>
      <div class="rs-stages">
        {stage(1, 'IKON', 'Promoter / event', 'The first commercial deployment: VYB in a real live-event environment. The objective is the first meaningful body of transaction and operational data showing VYB can function as financial infrastructure inside live commerce.', ['Event payments', 'Artist payments', 'Vendor payments', 'Settlement', 'Reconciliation', 'Financial reporting', 'Payment routing', 'Transaction-level data', 'Time-to-settlement'], 'VYB works in a live event environment.', 'var(--s1)')}
        {stage(2, 'Red Light Management', 'Artist / management', 'Moves VYB from an individual event environment into the artist-management and touring ecosystem — and from event infrastructure toward artist and entertainment financial infrastructure. The objective is to show VYB following the money across multiple counterparties in the same ecosystem.', ['Artists', 'Managers', 'Touring', 'Promoters', 'Venues', 'Vendors', 'Event-related expenses', 'Settlement', 'Artist business operations', 'Financial reporting'], 'VYB expands from individual events into the broader entertainment financial network.', 'var(--s2)')}
        {stage(3, 'Mercedes-Benz Stadium', 'Venue / operator', 'Institutional venue scale, from the venue and operator side of the ecosystem: orchestration, settlement and financial intelligence for a building that hosts everyone else’s events.', ['Venue payments', 'Event payments', 'Vendor payments', 'Talent payments', 'Payment orchestration', 'Settlement', 'Reconciliation', 'Event-level financial intelligence', 'Financial reporting', 'Working-capital / financing products', 'Real-time financial visibility'], 'VYB operates as financial infrastructure at institutional venue scale.', 'var(--s3)')}
      </div>
    </section>

    <section class="pl-sec" id="sequence">
      <div class="pl-sec-num">03 — WHY THE SEQUENCE MATTERS</div>
      <h2 class="pl-h">Promoter, then artist, then venue: VYB sits between all three.</h2>
      <p class="pl-lede">Substantially more powerful than accumulating customer logos: each deployment is a different side of the same transactions. Together they demonstrate that VYB can become the financial infrastructure connecting the participants who collectively create live commerce.</p>
      <div class="rs-arch" data-io="">
        <div class="rs-col">
          <div class="pl-sub-h">The deployments</div>
          <div class="fc-chain" style="margin-top:0;">
            <div class="cn"><div class="k">Stage 1</div><div class="v">IKON</div><div class="s">promoter / event</div></div><div class="ar">↓</div>
            <div class="cn"><div class="k">Stage 2</div><div class="v">Red Light Management</div><div class="s">artist / management</div></div><div class="ar">↓</div>
            <div class="cn"><div class="k">Stage 3</div><div class="v">Mercedes-Benz Stadium</div><div class="s">venue / operator</div></div>
          </div>
        </div>
        <div class="rs-col">
          <div class="pl-sub-h">The long-term architecture</div>
          <div class="rs-ladder">
            <div>Artist</div><div class="x">↕</div><div>Management</div><div class="x">↕</div><div>Promoter</div><div class="x">↕</div><div>Venue</div><div class="x">↕</div><div>Vendors</div>
          </div>
          <div class="rs-vyb"><span class="app-icon">v</span> VYB coordinates the financial activity between them.</div>
        </div>
      </div>
    </section>

    <section class="pl-sec" id="seed">
      <div class="pl-sec-num">04 — THE {money(SEED).upper()} SEED</div>
      <h2 class="pl-h">The appropriate amount at a reasonable valuation.</h2>
      <p class="pl-lede">The primary objective is a clean cap table and meaningful founder ownership going into the institutional round — not maximizing the seed valuation at the expense of future flexibility.</p>
      <div class="kpis" data-io="">
        {kpi(money(SEED), 'target raise')}
        {kpi(money(PRE), 'pre-money · illustrative')}
        {kpi(money(POST), 'post-money · target', '$25M–$30M post-money economics')}
        {kpi(pct(OWN), 'issued to new investors', 'before other capitalization considerations')}
      </div>
      <div class="fc-two" data-io="">
        <div>{kv([('Structure', f'A priced round is the base case: {money(PRE)} pre-money + {money(SEED)} new capital = {money(POST)} post-money.'), ('Alternative', 'A post-money SAFE, if strategically advantageous — counsel to evaluate dilution, cap-table implications, investor rights and future financing consequences before the instrument is chosen.'), ('Objective', 'Preserve founder ownership and enter the Series A with an institutionally attractive capitalization.')])}</div>
        <div class="fc-callout"><div class="fc-callout-h">What the seed is for</div><p>Production infrastructure. Strategic commercial deployments. Meaningful transaction volume. Recurring revenue. Proof that VYB operates across multiple layers of the ecosystem — the promoter, the artist’s management, the venue.</p></div>
      </div>
    </section>

    <section class="pl-sec" id="proceeds">
      <div class="pl-sec-num">05 — USE OF PROCEEDS</div>
      <h2 class="pl-h">{money(SEED)}, allocated.</h2>
      <div class="fc-chart-wrap" data-io="">{legend(USE)}{stack(USE, 'up-t', 'Seed use of proceeds')}</div>
      <div class="fc-table-wrap" data-io="">{table(USE, 'Use of proceeds')}</div>
      <div class="fc-callout" data-io=""><div class="fc-callout-h">Strategic commercial deployment &amp; market validation · {money(USE[3][1])}</div><p>Specifically intended to execute the commercial progression above. It is not funding an event. It is capital deployed to establish VYB’s financial infrastructure in a high-volume live environment and generate measurable commercial evidence.</p></div>
    </section>

    <section class="pl-sec" id="mission">
      <div class="pl-sec-num">06 — FORECAST → PROOF</div>
      <h2 class="pl-h">What the seed takes VYB from, and to.</h2>
      <div class="rs-mission" data-io="">
        <div class="m"><div class="pl-sub-h">Today</div>{chips(['Working proof of concept', 'Enterprise conversations', 'Strategic opportunities', 'Forecasted economics'])}</div>
        <div class="ar">→</div>
        <div class="m hi"><div class="pl-sub-h">Seed deployment</div>{chips(['IKON', 'Red Light Management', 'Mercedes-Benz Stadium'])}</div>
        <div class="ar">→</div>
        <div class="m"><div class="pl-sub-h">Result</div>{chips(['Live TPV', 'Recurring revenue', 'Enterprise customers', 'Payment economics', 'Settlement data', 'Reconciliation data', 'Financial data', 'Financing demand', 'Customer retention', 'Enterprise case studies'])}</div>
      </div>
    </section>

    <section class="pl-sec" id="economics">
      <div class="pl-sec-num">07 — THE ECONOMIC MODEL</div>
      <h2 class="pl-h">One enterprise relationship: {money(TPV1)} of volume, {money(REV['Base'])} → {money(REV['Medium'])} → {money(REV['Full'])}.</h2>
      <p class="pl-lede">The <a href="/forecast">VYB forecast</a> models one high-volume enterprise promoter at {money(TPV1)} of annual paid-out volume. VYB revenue expands as the platform moves deeper into that customer’s financial infrastructure — within the same underlying relationship.</p>
      <div class="fc-expand" data-io="">
        <div class="ex"><div class="t" style="color:var(--s1)">Base</div><div class="n">{money(REV['Base'])}</div><div class="m">software</div><div class="bar"><i style="width:{REV['Base']/REV['Full']*100:.1f}%;background:var(--s1)"></i></div></div>
        <div class="ex"><div class="t" style="color:var(--s2)">Medium</div><div class="n">{money(REV['Medium'])}</div><div class="m">payment orchestration · cards</div><div class="bar"><i style="width:{REV['Medium']/REV['Full']*100:.1f}%;background:var(--s2)"></i></div></div>
        <div class="ex hi"><div class="t" style="color:var(--s3)">Full</div><div class="n">{money(REV['Full'])}</div><div class="m">settlement · financing · intelligent operations</div><div class="bar"><i style="width:100%;background:var(--s3)"></i></div></div>
      </div>
      <div class="ik-hchain-lite" data-io="">Software → Payment orchestration → Cards → Settlement → Financing → Intelligent financial operations</div>
    </section>

    <section class="pl-sec" id="network">
      <div class="pl-sec-num">08 — NETWORK ECONOMICS</div>
      <h2 class="pl-h">A concentrated network of high-value relationships.</h2>
      <p class="pl-lede">Why the strategy is high-value enterprise relationships rather than customer count. At approximately {money(TPV1)} of annual volume per comparable relationship — illustrative scaling scenarios, not forecasts:</p>
      <div class="kpis" data-io="">{''.join(kpi(money(n*TPV1), f'{n} customers · TPV') for n in SCALE)}</div>
      <p class="pl-note">The strategic implication: VYB could build substantial transaction volume through a relatively small number of enterprise relationships. Revenue per customer, not customer count, is the first lever.</p>
    </section>

    <section class="pl-sec" id="seriesa">
      <div class="pl-sec-num">09 — THE INSTITUTIONAL SERIES A</div>
      <h2 class="pl-h">Not a $15M–$30M Series A. A $75M–$125M+ one, with $100M+ as the target.</h2>
      <p class="pl-lede">Raised after genuine product-market fit and repeatability, and sized to the metrics VYB has generated by then. The seed exists to make this round possible.</p>
      <div class="pl-sub-h" style="margin-top:30px;">Evidence to bring to the round · strategic targets, not forecasts or commitments</div>
      <div class="rs-grid" data-io="">
        <div><b>$500M–$1B+</b><span>annualized TPV</span></div>
        <div><b>$5M–$15M+</b><span>annualized revenue</span></div>
        <div><b>Strong</b><span>year-over-year growth</span></div>
        <div><b>Multiple</b><span>enterprise customers</span></div>
        <div><b>Strong</b><span>customer retention</span></div>
        <div><b>Rising</b><span>TPV per customer</span></div>
        <div><b>Expansion</b><span>revenue within accounts</span></div>
        <div><b>Rising</b><span>share of customer financial activity routed through VYB</span></div>
        <div><b>Demonstrated</b><span>payment take rate</span></div>
        <div><b>Demonstrated</b><span>settlement and reconciliation savings</span></div>
        <div><b>Demonstrated</b><span>card economics</span></div>
        <div><b>Demonstrated</b><span>financing demand</span></div>
        <div><b>Proven</b><span>enterprise implementation process</span></div>
        <div><b>Strong</b><span>strategic partnerships</span></div>
      </div>
    </section>

    <section class="pl-sec" id="narrative">
      <div class="pl-sec-num">10 — THE NARRATIVE CHANGES</div>
      <h2 class="pl-h">The investor conversation evolves with each deployment.</h2>
      <div class="pl-rows">
        <div class="pl-row" data-io=""><div class="r-i">01</div><div class="r-t">Seed</div><div class="r-d">VYB is building the financial operating system for live commerce.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">02</div><div class="r-t">After IKON</div><div class="r-d">VYB has demonstrated its financial infrastructure in a live event environment.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">03</div><div class="r-t">After Red Light Management</div><div class="r-d">VYB is expanding from event infrastructure into the artist and management ecosystem.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">04</div><div class="r-t">After Mercedes-Benz Stadium</div><div class="r-d">VYB has demonstrated its infrastructure across multiple sides of the live-commerce ecosystem.</div></div>
        <div class="pl-row" data-io=""><div class="r-i">05</div><div class="r-t">Series A</div><div class="r-d"><b>VYB has proven the model and is now scaling a financial network.</b> That is the transformation the seed is meant to create.</div></div>
      </div>
    </section>

    <section class="pl-sec" id="deploy">
      <div class="pl-sec-num">11 — SERIES A DEPLOYMENT</div>
      <h2 class="pl-h">A $100M round accelerates a proven network. It does not extend runway.</h2>
      <p class="pl-lede">A potential allocation; the exact split would depend on business conditions at the time.</p>
      <div class="fc-chart-wrap" data-io="">{legend(SERIES_A)}{stack(SERIES_A, 'sa-t', 'Series A deployment')}</div>
      <div class="fc-table-wrap" data-io="">{table(SERIES_A, 'Series A deployment · $100M')}</div>
    </section>

    <section class="pl-sec" id="capital">
      <div class="pl-sec-num">12 — EQUITY VS. FINANCING CAPITAL</div>
      <h2 class="pl-h">Corporate equity builds the company. Structured capital finances the commerce.</h2>
      <p class="pl-lede">Long term, VYB distinguishes between the two — so financial products can scale without equivalent shareholder dilution.</p>
      <div class="fc-two" data-io="">
        <div class="fc-callout"><div class="fc-callout-h">Equity capital</div>{chips(['Employees', 'Engineering', 'Product', 'Sales', 'Infrastructure', 'Expansion', 'Strategic acquisitions'])}</div>
        <div class="fc-callout"><div class="fc-callout-h">Debt · warehouse · structured capital</div>{chips(['Customer financing', 'Receivables', 'Working capital', 'Event financing', 'Other financial products'])}</div>
      </div>
      <p class="pl-note">See the <a href="/forecast#capital">forecast’s capital-efficiency section</a>: in the modeled Full integration, a capital partner funds each advance and VYB originates and services it — capital facilitated, not capital deployed.</p>
    </section>

    <section class="pl-sec" id="roadmap">
      <div class="pl-sec-num">13 — LONG-TERM CAPITAL ROADMAP</div>
      <h2 class="pl-h">Build, prove, scale, expand, finance.</h2>
      <div class="fc-chain" data-io="">
        <div class="cn wide"><div class="k">{money(SEED)} seed · build + prove</div><div class="v">IKON → Red Light Management → Mercedes-Benz Stadium</div></div><div class="ar">↓</div>
        <div class="cn wide"><div class="k">Product-market fit</div><div class="v">prove repeatability</div></div><div class="ar">↓</div>
        <div class="cn wide hi"><div class="k">$75M–$125M+ Series A</div><div class="v">scale the financial network</div></div><div class="ar">↓</div>
        <div class="cn wide"><div class="k">$150M–$300M+ Series B</div><div class="v">expand infrastructure + market</div></div><div class="ar">↓</div>
        <div class="cn wide"><div class="k">Growth / strategic capital</div><div class="v">category expansion</div></div><div class="ar">↓</div>
        <div class="cn wide"><div class="k">Debt · warehouse · structured facilities</div><div class="v">finance the underlying commerce</div></div>
      </div>
    </section>

    <section class="pl-sec" id="captable">
      <div class="pl-sec-num">14 — FOUNDER / CAP TABLE OBJECTIVE</div>
      <h2 class="pl-h">Avoid unnecessary dilution at the seed. Enter the Series A clean.</h2>
      <p class="pl-lede">Raise the appropriate amount at a reasonable valuation and use it to create a major increase in enterprise value — rather than maximize the seed valuation at the expense of future flexibility.</p>
      <div class="pl-sub-h" style="margin-top:30px;">For counsel to model</div>
      {chips(['Founder ownership after the seed', 'Existing capitalization', 'Option pool', 'SAFE vs. priced-round dilution', 'Pro-rata rights', 'Future Series A dilution', 'Series A option-pool refresh', 'Board rights', 'Investor protective provisions', 'Liquidation preferences', 'Conversion mechanics', 'Future debt / warehouse financing', 'Strategic investor rights'])}
      <p class="pl-note">Objective: enter the eventual $100M+ Series A with a clean, institutionally attractive capitalization structure.</p>
    </section>

    <section class="pl-sec" id="philosophy">
      <div class="pl-sec-num">15 — CAPITAL PHILOSOPHY</div>
      <h2 class="pl-h">From a startup with a compelling forecast to a proven financial infrastructure company.</h2>
      <p class="pl-lede">IKON provides the initial live-event proof. Red Light Management expands VYB into the artist-management and touring ecosystem. Mercedes-Benz Stadium validates VYB at institutional venue scale. Together: <b>Artist → Management → Promoter → Venue → Vendor.</b> The resulting transaction volume, financial data and customer relationships establish product-market fit — and at that point the Series A is capital for scaling an existing network, not for proving one can exist.</p>
      <div class="rs-phil" data-io="">
        <div><b>{money(SEED)}</b><span>Prove</span></div>
        <div><b>$100M+</b><span>Scale</span></div>
        <div><b>Debt · warehouse</b><span>Finance</span></div>
        <div class="hi"><b>Long term</b><span>Own the financial layer of live commerce</span></div>
      </div>
      <div class="pl-cta" style="margin-top:40px;">
        <div class="pl-cta-card" data-io=""><h3>The economics behind the plan</h3><p>One enterprise customer, three depths of integration, and what happens at 10, 25, 50 and 100.</p><a href="/forecast">Read the forecast →</a></div>
        <div class="pl-cta-card" data-io=""><h3>Talk to the founder</h3><p>Blake Jackovitch · Founder, VYB.</p><a href="mailto:blake@vybapp.io?subject=VYB%20seed">blake@vybapp.io →</a></div>
      </div>
      <p class="pl-note">Strategic targets and illustrative structures, not forecasts, commitments, or an offer to sell securities. Named relationships are targets at their respective stages.</p>
    </section>

  </main>
</div>
</div>

<footer>
  <div class="footer-inner">
    <div><div class="footer-brand"><span class="app-icon">v</span> vyb</div><div class="footer-meta">© 2026 VYB · CAPITAL STRATEGY · CONFIDENTIAL</div></div>
    <div class="footer-links"><a href="/">Home</a><a href="/forecast">Forecast</a><a href="/pulse">VYB Pulse</a><a href="mailto:blake@vybapp.io?subject=VYB%20seed">Contact</a></div>
  </div>
</footer>
"""

TITLE = "VYB — Raise"
DESC = "VYB's capital strategy: a $5M seed that funds three strategic commercial deployments and turns a forecast into proof, ahead of a $100M+ institutional Series A."
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
<meta property="og:url" content="https://vybapp.io/raise">
<link rel="canonical" href="https://vybapp.io/raise">
<style>{css}{extra}</style>
</head>
<body>
{body}
<script>
{js}
</script>
</body></html>
"""
open(OUT, 'w', encoding='utf-8').write(page)
print(f"wrote {OUT} ({len(page)} bytes)")
