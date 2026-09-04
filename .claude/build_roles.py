#!/usr/bin/env python3
"""Assemble /Users/b/Projects/vyb-web/roles.html — three founding-stage roles.
Reuses site.css + pulse_extra.css + forecast_extra.css + raise_extra.css + roles_extra.css."""
import os, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/Users/b/Projects/vyb-web/roles.html'

META = [('Location', 'Atlanta, GA · hybrid or remote'), ('Employment', 'Full-time'), ('Level', 'Executive / senior leadership'), ('Reports to', 'Founder & CEO')]

def chips(items, cls=''):
    return f'<div class="pl-chips {cls}">' + ''.join(f'<span class="pl-chip">{i}</span>' for i in items) + '</div>'
def cols(groups):
    return '<div class="pl-pass">' + ''.join(f'<div class="pl-pass-col"><h3>{h}</h3><ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul></div>' for h, items in groups) + '</div>'
def bullets(items):
    return '<ul class="fc-list">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
def kv(rows):
    return '<div class="fc-kv">' + ''.join(f'<div class="fc-kv-row"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in rows) + '</div>'

ROLES = [
 dict(id='payments', num='02', col='var(--s1)', short='Payments', title='Head of Payments &amp; Financial Infrastructure', tag='You own the money.',
  about='The live entertainment economy moves billions of dollars across artists, managers, promoters, venues, studios, vendors, production companies and other counterparties — on infrastructure fragmented across processors, banks, ticketing platforms, accounting systems, spreadsheets and disconnected workflows. VYB connects those flows into one intelligent system: existing rails first, then deeper orchestration, financial infrastructure, cards, settlement, reconciliation and eventually payment-facilitation capabilities.',
  role='A senior payments executive to own the architecture and evolution of VYB’s financial infrastructure. A foundational role: you determine how money moves through VYB, how transactions are represented and reconciled, how merchants and counterparties are onboarded, how funds settle, and how VYB progressively owns more of the economics and infrastructure underneath live commerce. You have built payment infrastructure at scale and understand both the technical and regulatory dimensions.',
  own=[('Payment infrastructure', ['Design VYB’s payment orchestration architecture', 'Define integrations with processors, acquiring partners and banking infrastructure', 'Develop payment routing strategies', 'Design merchant / sub-merchant architecture', 'Evaluate the path from processor-dependent infrastructure toward PayFac capabilities', 'Build resilient payment flows for high-volume event environments']),
       ('Ledger, settlement &amp; reconciliation', ['Architect VYB’s financial ledger', 'Build transaction-level accounting infrastructure', 'Design automated reconciliation between VYB, processors, banks, merchants and enterprise systems', 'Develop settlement workflows', 'Create real-time visibility into transaction status and cash movement', 'Establish controls around exceptions, disputes and failed payments']),
       ('Financial products', ['Virtual cards', 'Commercial cards', 'ACH / RTP capabilities', 'Payout infrastructure', 'Working-capital products', 'Event financing infrastructure', 'Receivables-based financing', 'Future products built on VYB transaction data']),
       ('Risk &amp; compliance', ['KYC / KYB', 'AML controls', 'Transaction monitoring', 'PCI requirements', 'Merchant underwriting', 'Fraud controls', 'Chargeback and dispute processes', 'Financial controls', 'Sponsor-bank requirements']),
       ('Banking &amp; infrastructure relationships', ['Sponsor banks', 'Payment processors', 'Acquirers', 'Card networks', 'Banking-as-a-service providers', 'Financial infrastructure providers', 'Capital partners'])],
  success_h='What success looks like · first 12–18 months',
  success=['Production-grade payment infrastructure established', 'Meaningful enterprise transaction volume processed', 'Reliable reconciliation and settlement', 'Banking and processing relationships established', 'Reduced dependence on fragmented third-party infrastructure', 'Initial financial products launched', 'The architecture required for future PayFac capabilities', 'The foundation for financing and underwriting', 'The financial data layer required for intelligent automation'],
  ideal=['8–15+ years of payments / fintech experience', 'Experience at a major payments, banking or financial infrastructure company', 'Deep understanding of acquiring and payment processing', 'Experience with payment orchestration or PayFac infrastructure', 'Strong understanding of financial ledgers and reconciliation', 'Experience launching production financial products', 'Strong regulatory and compliance awareness', 'Experience working with banks and financial institutions', 'Ability to explain complex financial infrastructure to non-financial engineers and executives'],
  valuable='Experience at companies such as Stripe, Adyen, Block, PayPal, Fiserv, JPMorgan or similar is valuable — but the quality of your experience matters more than the logo. You should be someone who has <b>actually built and operated financial infrastructure</b>, not simply sold it.',
  who=['You are comfortable operating without a massive team.', 'You can move from a conversation with a sponsor bank to an architecture discussion with engineers to a regulatory discussion with counsel.', 'You understand that VYB is not trying to become another generic payments company. The goal is to build the financial infrastructure underneath an entirely new category of commerce.']),
 dict(id='enterprise', num='03', col='var(--s2)', short='Enterprise', title='Head of Enterprise &amp; Strategic Partnerships', tag='You own the customers.',
  about='VYB’s customers operate across the interconnected ecosystem of artists, management companies, promoters, venues, studios, vendors and event operators. The opportunity is to replace fragmented financial workflows with a unified platform for payments, settlement, reconciliation, financial intelligence and eventually embedded financial services.',
  role='An exceptional enterprise operator to build VYB’s strategic commercial engine — turning early relationships and deployments into repeatable enterprise distribution. You work directly with the founder and with senior executives across entertainment, sports, venues, hospitality, payments and financial services. This is not a traditional sales position: you need to understand how complex organizations operate financially and sell a transformation rather than a software license.',
  mandate='Build VYB’s enterprise network across <b>promoters → artists → management → venues → vendors → financial institutions</b>. The initial strategic progression runs <b>IKON → Red Light Management → Mercedes-Benz Stadium</b> — each a different layer of the live-commerce ecosystem.',
  own=[('Enterprise sales · the complete process', ['Account identification', 'Executive relationship development', 'Discovery', 'Solution development', 'Pilot structuring', 'Commercial negotiations', 'Contracting', 'Deployment', 'Expansion']),
       ('Strategic partnerships', ['Promoters', 'Venue operators', 'Stadiums', 'Management companies', 'Artist organizations', 'Studios', 'Ticketing companies', 'Hospitality operators', 'Payment companies', 'Banks', 'Financial institutions', 'Technology providers']),
       ('Enterprise deployment · what you will understand', ['How customers currently move money', 'Where financial fragmentation occurs', 'Where reconciliation breaks', 'Where settlement slows down', 'Where money is unnecessarily trapped', 'Where financing is required', 'Where VYB can create measurable economic value']),
       ('Commercial expansion', ['The objective is not to land customers; it is to expand VYB’s economic footprint within each one', 'Software → payments → cards → settlement → financing → financial intelligence', 'Constantly identify the next layer of the customer’s financial infrastructure VYB can move into'])],
  success_h='Key metrics',
  success=['Enterprise customers acquired', 'Enterprise pilots launched', 'Pilot-to-contract conversion', 'Annual contract value', 'Payment volume routed', 'Revenue generated', 'Financial workflows moved onto VYB', 'Expansion revenue', 'Customer retention', 'Strategic partnerships established', 'Enterprise deployment time'],
  ideal=['8–15+ years of enterprise fintech, payments or financial-services experience', 'Experience selling complex B2B infrastructure', 'Experience with enterprise executives', 'Strong understanding of payments or financial operations', 'Experience with large merchants, venues, hospitality, entertainment or sports is highly valuable', 'Demonstrated ability to close complex enterprise transactions', 'Strong strategic partnership experience'],
  valuable='Experience selling into stadiums, promoters, entertainment companies, hospitality groups, sports organizations, financial institutions or large merchants is highly relevant.',
  who=['You are commercially aggressive without being transactional.', 'You can sit with a CFO and discuss financial economics, then sit with an operations team and understand workflow problems.', 'You know how to get a pilot started quickly and how to turn it into a long-term institutional relationship.', 'You are comfortable with ambiguity and building the sales process as you go.', 'Most importantly, you understand that VYB’s competitive advantage is not software. It is <b>the network created by connecting financial activity across the live-commerce ecosystem.</b>']),
 dict(id='product', num='04', col='var(--s3)', short='Product &amp; AI', title='Head of Product, AI &amp; Financial Systems', tag='You own the intelligence layer.',
  about='VYB combines payments, financial data, operational workflows and AI into a system capable of understanding — and eventually orchestrating — the financial activity of live entertainment businesses. The long-term product vision is <b>data → intelligence → agent → action</b>: beyond showing a business what happened, the platform understands what is happening, determines what needs to happen next and, where authorized, executes the appropriate financial workflow.',
  role='A senior product leader to own that evolution, working across product, engineering, payments, finance and enterprise customers to build the intelligence layer on top of VYB’s financial infrastructure. A founding product leadership position: you help define what VYB becomes.',
  own=[('The financial operating system · one representation of the business', ['Payments', 'Transactions', 'Contracts', 'Events', 'Vendors', 'Artists', 'Venues', 'Expenses', 'Settlement', 'Reconciliation', 'Reporting', 'Cash flow', 'Financing']),
       ('AI &amp; agentic financial workflows', ['Monitoring financial obligations', 'Identifying upcoming payments', 'Understanding contracts', 'Reconciling transactions', 'Detecting anomalies', 'Forecasting cash requirements', 'Identifying financial leakage', 'Recommending payment actions', 'Preparing approvals', 'Initiating authorized transactions']),
       ('Product architecture · requirements across', ['APIs', 'Financial data models', 'Transaction infrastructure', 'User permissions', 'Workflow engines', 'AI agents', 'Enterprise dashboards', 'Reporting', 'Integrations', 'Payment workflows', 'Reconciliation', 'Financial intelligence']),
       ('Customer development · time in the field with', ['Promoters', 'Artists', 'Managers', 'Venue operators', 'Finance teams', 'Studios', 'Vendors', 'Goal: find the repetitive financial workflows that can be consolidated and automated'])],
  philosophy='VYB should not become another dashboard. A dashboard tells an operator what happened. VYB should increasingly tell the operator <b>what happened, why it happened, what is going to happen, what needs to happen next — and, when authorized, execute it.</b> From software that records financial activity to software that understands and orchestrates it.',
  success_h='Key metrics',
  success=['Product adoption', 'Active enterprise users', 'Financial workflows automated', 'Percentage of transactions automatically reconciled', 'Payment workflows automated', 'Time saved per customer', 'Reduction in financial leakage', 'Time-to-settlement', 'Customer expansion', 'AI agent utilization', 'Accuracy of automated recommendations', 'Percentage of financial activity orchestrated through VYB'],
  ideal=['8–15+ years of product experience', 'Senior product leadership experience', 'Fintech, payments, financial infrastructure or vertical SaaS background', 'Strong understanding of APIs and platform products', 'Experience building enterprise software', 'Experience with AI / agentic systems', 'Strong understanding of financial data', 'Experience working closely with engineering teams', 'Demonstrated ability to take products from concept to production'],
  valuable='Experience building payments products, financial operating systems, ERP / financial software, vertical SaaS, AI agents, workflow automation, enterprise APIs or transaction-based platforms is especially valuable.',
  who=['You are technical enough to understand architecture but product-oriented enough to obsess over the customer.', 'You don’t believe AI should simply be added to a product as a feature; you understand how it fundamentally changes the way financial software operates.', 'You are comfortable taking a messy real-world workflow and turning it into a simple product.', 'You are willing to spend time in the field with customers rather than designing the product from a conference room.']),
]

def role_section(r):
    subj = urllib.parse.quote('VYB — ' + r['title'].replace('&amp;', '&'))
    parts = [f'''
    <section class="pl-sec rl-role" id="{r['id']}">
      <div class="pl-sec-num" style="color:{r['col']}">{r['num']} — {r['short'].upper()}</div>
      <h2 class="pl-h" style="max-width:none;">{r['title']}</h2>
      <div class="rl-meta" data-io="">{''.join(f'<div><span class="k">{k}</span><span class="v">{v}</span></div>' for k, v in META)}</div>
      <div class="pl-sub-h" style="margin-top:30px;">About VYB, for this role</div>
      <p class="pl-lede">{r['about']}</p>
      <div class="pl-sub-h" style="margin-top:30px;">The role</div>
      <p class="pl-lede">{r['role']}</p>''']
    if r.get('mandate'): parts.append(f'<div class="fc-callout" data-io=""><div class="fc-callout-h">Strategic mandate</div><p>{r["mandate"]}</p></div>')
    parts.append(f'<div class="pl-sub-h" style="margin-top:30px;">What you will own</div><div data-io="">{cols(r["own"])}</div>')
    if r.get('philosophy'): parts.append(f'<div class="fc-callout" data-io=""><div class="fc-callout-h">Product philosophy</div><p>{r["philosophy"]}</p></div>')
    parts.append(f'''
      <div class="fc-two" style="margin-top:34px;" data-io="">
        <div><div class="pl-sub-h">{r['success_h']}</div>{chips(r['success'])}</div>
        <div><div class="pl-sub-h">Ideal candidate</div>{bullets(r['ideal'])}<p class="pl-note"><b>Particularly valuable.</b> {r['valuable']}</p></div>
      </div>
      <div class="pl-sub-h" style="margin-top:34px;">Who you are</div>
      <div class="pl-quotes" data-io="">{''.join(f'<q>{w}</q>' for w in r['who'])}</div>
      <div class="rl-tag" data-io="" style="border-color:{r['col']}"><span style="color:{r['col']}">{r['tag']}</span><a href="mailto:blake@vybapp.io?subject={subj}" class="pl-btn">Apply · {r['title'].replace('&amp;','&').replace('Head of ','')} →</a></div>
    </section>''')
    return '\n'.join(parts)

css = open(os.path.join(HERE, 'site.css')).read()
extra = ''.join(open(os.path.join(HERE, f)).read() for f in ['pulse_extra.css', 'forecast_extra.css', 'raise_extra.css', 'roles_extra.css'])
js = open(os.path.join(HERE, 'build_pulse.py')).read().split('js = """')[1].split('"""')[0]

body = f"""<nav>
  <a href="/" class="nav-logo"><span class="app-icon">v</span> vyb</a>
  <div class="nav-right">
    <a href="/#features" class="nav-link">Features</a>
    <a href="/#enterprise" class="nav-link">Enterprise</a>
    <a href="/forecast" class="nav-link">Forecast</a>
    <a href="/roles" class="nav-link" aria-current="page">Roles</a>
    <a href="mailto:blake@vybapp.io?subject=VYB%20roles" class="nav-buy-btn">Apply</a>
    <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode"><span class="tt-icon tt-sun">☀️</span><span class="tt-icon tt-moon">🌙</span></button>
  </div>
</nav>

<div class="pl-page">

<header class="pl-hero" id="top">
  <div class="pl-hero-inner">
    <p class="pl-kicker">Roles · founding team</p>
    <h1>Three founding-stage roles. Rails, distribution, intelligence.</h1>
    <p class="pl-sub">VYB is building the financial operating system for live commerce. We are hiring three senior, hands-on leaders to build it — each with a clear mandate, measurable outcomes, and the authority to build the function. <em>Payments</em> owns the rails. <em>Enterprise</em> owns distribution. <em>Product &amp; AI</em> owns the intelligence layer.</p>
    <div class="pl-hero-actions">
      <a href="#payments" class="pl-btn">Head of Payments →</a>
      <a href="#enterprise" class="pl-btn-ghost">Head of Enterprise</a>
      <a href="#product" class="pl-btn-ghost">Head of Product, AI &amp; Financial Systems</a>
    </div>
    <div class="pl-strip">
      <div><div class="n">3<span class="u">executive roles</span></div><div class="l">Founding-stage, reporting to the founder &amp; CEO.</div></div>
      <div><div class="n">ATL<span class="u">Atlanta, GA</span></div><div class="l">Hybrid or remote.</div></div>
      <div><div class="n">8–15+<span class="u">years</span></div><div class="l">Payments, fintech, enterprise or product leadership.</div></div>
      <div><div class="n">1<span class="u">system</span></div><div class="l">Rails, customers and intelligence on one ledger.</div></div>
    </div>
  </div>
</header>

<div class="pl-shell">
  <aside class="pl-rail">
    <div class="pl-rail-h">The roles</div>
    <div id="plRail" class="pl-rail-nav">
      <a href="#about"><span class="i">01</span> About VYB</a>
      <a href="#payments"><span class="i">02</span> Payments &amp; financial infrastructure</a>
      <a href="#enterprise"><span class="i">03</span> Enterprise &amp; strategic partnerships</a>
      <a href="#product"><span class="i">04</span> Product, AI &amp; financial systems</a>
      <a href="#fit"><span class="i">05</span> How they fit</a>
      <a href="#apply"><span class="i">06</span> Apply</a>
    </div>
  </aside>

  <main class="pl-main">

    <section class="pl-sec" id="about">
      <div class="pl-sec-num">01 — ABOUT VYB</div>
      <h2 class="pl-h">The financial operating system for live commerce.</h2>
      <p class="pl-lede">The live entertainment economy moves billions of dollars across artists, managers, promoters, venues, studios, vendors, production companies and other counterparties. The financial infrastructure underneath it is fragmented across payment processors, banks, ticketing platforms, accounting systems, spreadsheets and disconnected operational workflows. VYB connects those flows into one intelligent system — payments, settlement, reconciliation, financial intelligence and, in time, embedded financial services.</p>
      <div class="fc-levels" data-io="">
        <div class="fc-level"><div class="t" style="color:var(--s1)">Payments</div><div class="c" style="font-size:22px;">Owns the rails</div><div class="d">How money moves through VYB, how it is represented and reconciled, how it settles, and how VYB progressively owns more of the infrastructure underneath live commerce.</div></div>
        <div class="fc-level"><div class="t" style="color:var(--s2)">Enterprise</div><div class="c" style="font-size:22px;">Owns distribution</div><div class="d">Turns early relationships into repeatable enterprise distribution and expands VYB’s economic footprint inside every customer.</div></div>
        <div class="fc-level"><div class="t" style="color:var(--s3)">Product &amp; AI</div><div class="c" style="font-size:22px;">Owns the intelligence layer</div><div class="d">Data → intelligence → agent → action: from software that records financial activity to software that understands and orchestrates it.</div></div>
      </div>
      <p class="pl-note">These are senior, hands-on roles, not corporate job descriptions. Each comes with a clear mandate, measurable outcomes and enough authority to actually build the function. Read the <a href="/forecast">forecast</a> and the <a href="/raise">capital strategy</a> for the economics and the plan behind them.</p>
    </section>

    {''.join(role_section(r) for r in ROLES)}

    <section class="pl-sec" id="fit">
      <div class="pl-sec-num">05 — HOW THEY FIT</div>
      <h2 class="pl-h">Deliberately complementary.</h2>
      <p class="pl-lede">Payments owns the rails. Enterprise owns distribution. Product and AI owns the intelligence layer. Each reports to the founder; each builds its function from the ground up; each is measured on outcomes the other two depend on.</p>
      <div class="fc-chain" data-io="">
        <div class="cn wide"><div class="k" style="color:var(--s2)">Enterprise</div><div class="v">Brings the customer and the workflow: where money moves, where it breaks, where VYB creates measurable value.</div></div><div class="ar">↓</div>
        <div class="cn wide"><div class="k" style="color:var(--s3)">Product &amp; AI</div><div class="v">Turns that workflow into one financial representation of the business, and into agents that watch, recommend and — when authorized — act.</div></div><div class="ar">↓</div>
        <div class="cn wide"><div class="k" style="color:var(--s1)">Payments</div><div class="v">Moves and settles the money underneath, on rails VYB progressively owns, with the ledger, controls and banking relationships to do it at enterprise scale.</div></div><div class="ar">↓</div>
        <div class="cn wide hi"><div class="k">Together</div><div class="v">The financial infrastructure underneath a new category of commerce.</div></div>
      </div>
    </section>

    <section class="pl-sec" id="apply">
      <div class="pl-sec-num">06 — APPLY</div>
      <h2 class="pl-h">Write to the founder.</h2>
      <p class="pl-lede">No portal. Send a short note on what you have built and operated, and which of the three you want to own.</p>
      <div class="pl-cta">
        {''.join(f'<div class="pl-cta-card" data-io=""><h3>{r["title"]}</h3><p>{r["tag"]}</p><a href="mailto:blake@vybapp.io?subject={urllib.parse.quote("VYB — " + r["title"].replace("&amp;", "&"))}">blake@vybapp.io →</a></div>' for r in ROLES)}
      </div>
      <p class="pl-note">Atlanta, GA · hybrid or remote · full-time · reporting to the founder &amp; CEO.</p>
    </section>

  </main>
</div>
</div>

<footer>
  <div class="footer-inner">
    <div><div class="footer-brand"><span class="app-icon">v</span> vyb</div><div class="footer-meta">© 2026 VYB · ROLES</div></div>
    <div class="footer-links"><a href="/">Home</a><a href="/forecast">Forecast</a><a href="/raise">Raise</a><a href="mailto:blake@vybapp.io?subject=VYB%20roles">Contact</a></div>
  </div>
</footer>
"""

TITLE = "VYB — Roles"
DESC = "Three founding-stage roles at VYB, the financial operating system for live commerce: Head of Payments & Financial Infrastructure, Head of Enterprise & Strategic Partnerships, Head of Product, AI & Financial Systems."
page = f"""<!DOCTYPE html>
<html lang="en" data-theme="light"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#ffffff" id="themeColorMeta">
<meta name="color-scheme" content="light dark">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://vybapp.io/roles">
<link rel="canonical" href="https://vybapp.io/roles">
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
