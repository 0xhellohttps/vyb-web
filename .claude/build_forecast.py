#!/usr/bin/env python3
"""Assemble /Users/b/Projects/vyb-web/forecast.html — the institutional case for VYB
built on one promoter's economics: TPV → monetization layers → revenue per
customer → platform scale. All figures are computed here from the
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
    if abs(x) >= 1e9: return f'${x/1e9:.{1 if d==0 else d}f}B'
    if abs(x) >= 1e6: return f'${x/1e6:.{1 if d==0 else d}f}M'
    if abs(x) >= 1e4: return f'${x/1e3:.0f}K'
    if abs(x) >= 1e3: return f'${x/1e3:.1f}K'
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


# ---------------------------------------------------------------- page (see build_forecast_page.py)
exec(open(os.path.join(HERE, 'build_forecast_page.py')).read())
