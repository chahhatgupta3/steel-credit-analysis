import sqlite3, pandas as pd

conn = sqlite3.connect('db/credit.db')
w = pd.read_sql('SELECT * FROM v_wide', conn)
f = pd.read_sql('SELECT * FROM financials', conn)
rows = []

def check(name, i, y, ok, detail=''):
    rows.append({'check': name, 'issuer': i, 'year': y, 'status': 'PASS' if ok else 'FAIL', 'detail': detail})

for _, r in w.iterrows():
    i, y = r['issuer'], r['fiscal_year']
    fi = f[(f.issuer == i) & (f.fiscal_year == y)]
    n = int(fi.value_inr_cr.notna().sum())
    check('completeness (13 items)', i, y, n == 13, str(n) + '/13')
    if n == 0:
        continue
    src_ok = fi.source_doc.fillna('').str.len().gt(0).all() and fi.page_no.notna().all()
    check('source + page documented', i, y, bool(src_ok))
    if n < 13:
        continue
    eb = r.pbt + r.finance_costs + r.depreciation + r.exceptional_items
    d = abs(eb - r.ebitda_reported) / r.ebitda_reported
    check('EBITDA recompute within 5%', i, y, d <= 0.05, 'diff ' + str(round(d * 100)) + '%')
    nd = r.total_borrowings - r.cash - r.other_bank - r.cur_inv
    check('net debt > 0', i, y, nd > 0, str(round(nd)))
    check('leverage between 0 and 10x', i, y, 0 < nd / eb < 10, str(round(nd / eb, 2)) + 'x')
    check('equity < total assets', i, y, r.total_equity < r.total_assets)
    check('OCF positive', i, y, r.ocf > 0)

out = pd.DataFrame(rows)
out.to_csv('outputs/quality_report.csv', index=False)
pd.set_option('display.width', 220)
print(out.to_string(index=False))
p = int((out.status == 'PASS').sum())
print('Pass rate:', p, '/', len(out))
