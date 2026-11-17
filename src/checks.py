import sqlite3, pandas as pd

conn = sqlite3.connect('db/credit.db')
w = pd.read_sql('SELECT * FROM v_wide', conn)
f = pd.read_sql('SELECT * FROM financials', conn)
rows = []

def check(name, issuer, ok, detail=''):
    rows.append({'check': name, 'issuer': issuer, 'status': 'PASS' if ok else 'FAIL', 'detail': detail})

for _, r in w.iterrows():
    i = r['issuer']
    fi = f[f.issuer == i]
    n = int(fi.value_inr_cr.notna().sum())
    check('completeness (13 items)', i, n == 13, f'{n}/13')
    check('source + page documented', i, bool(fi[['source_doc', 'page_no']].notna().all().all()))
    eb = r.pbt + r.finance_costs + r.depreciation + r.exceptional_items
    d = abs(eb - r.ebitda_reported) / r.ebitda_reported
    check('EBITDA recompute within 5%', i, d <= 0.05, f'model {eb:,.0f} vs reported {r.ebitda_reported:,.0f} ({d:.0%} diff)')
    nd = r.total_borrowings - r.cash - r.other_bank - r.cur_inv
    check('net debt > 0', i, nd > 0, f'{nd:,.0f}')
    check('leverage between 0 and 10x', i, 0 < nd / eb < 10, f'{nd / eb:.2f}x')
    check('equity < total assets', i, r.total_equity < r.total_assets)
    check('OCF positive', i, r.ocf > 0)

out = pd.DataFrame(rows)
out.to_csv('outputs/quality_report.csv', index=False)
pd.set_option('display.width', 220); pd.set_option('display.max_colwidth', 80)
print(out.to_string(index=False))
p = int((out.status == 'PASS').sum())
print(f'\nPass rate: {p}/{len(out)} = {p / len(out):.0%}')
