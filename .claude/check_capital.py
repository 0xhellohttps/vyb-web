#!/usr/bin/env python3
"""check_capital.py — drift check: every capital document must carry the figures in capital.json
and none of the retired ones. Run after editing any capital page: python3 .claude/check_capital.py"""
import json, re, sys, html
C = json.load(open('/Users/b/Projects/vyb-ios/docs/strategy/capital.json'))
def m(x): return f"${x/1e6:g}M"
s, a, f, g = C['seed'], C['series_a'], C['credit_facility'], C['growth_round_optional']
EXPECT = [m(s['amount']), m(s['pre_money']), m(s['post_money']), m(a['amount']), m(a['pre_money']), m(f['initial']), m(f['accordion'])+'+', 'IKON']
RETIRED = [r'\$5M seed', r'\$25M pre-money', r'\$30M post', r'\$7M', r'\$75[–-]\$?125M', r'\$100M\+ Series A', r'\$100M\+ institutional', r'\$150M[–-]\$?300M', r'\$15M[–-]\$?25M of equity', r'IKON \S* ?→ Red Light Management → Mercedes', r'IKON.{0,40}Red Light Management.{0,40}Mercedes-Benz Stadium']
DOCS = {
 'raise page':           '/Users/b/Projects/vyb-web/marketing/plain/raise.html',
 'investment deck':      '/Users/b/Projects/vyb-web/marketing/investor/investment-deck.html',
 'founder approach':     '/Users/b/Projects/vyb-ios/docs/strategy/founder-approach.html',
 'ikon strategy':        '/Users/b/Projects/vyb-ios/docs/strategy/ikon-strategy.html',
 'governance':           '/Users/b/Projects/vyb-ios/docs/strategy/governance.html',
 'payfac positioning':   '/Users/b/Projects/vyb-ios/docs/strategy/payfac-seed-positioning.md',
 'runway':               '/Users/b/Projects/vyb-ios/docs/strategy/runway.html',
}
def text(p):
    t=open(p,encoding='utf-8').read(); t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S); t=re.sub(r'<[^>]+>',' ',t); return re.sub(r'\s+',' ',html.unescape(t))
bad=0
for name,p in DOCS.items():
    t=text(p); miss=[e for e in EXPECT if e not in t]; hit=[r for r in RETIRED if re.search(r,t)]
    if name in ('governance','payfac positioning','runway'): miss=[x for x in miss if x not in (m(s['post_money']),)]
    # allow the retirement note in payfac positioning ("$7M figure ... is retired")
    if name=='payfac positioning': hit=[h for h in hit if h!=r'\$7M']
    # governance's ownership floor: the founder's dilution table has "$25M pre" nowhere; fine
    status='ok' if not miss and not hit else 'DRIFT'
    if status=='DRIFT': bad+=1
    print(f"{status:5s} {name:20s}" + (f"  missing {miss}" if miss else '') + (f"  retired {hit}" if hit else ''))
print('partner order:', ' → '.join(C['partner_order']))
sys.exit(1 if bad else 0)
