import sqlite3, pandas as pd
from common import get_year

T = 4.5
c = sqlite3.connect('db/credit.db')
Y = get_year(c)
r = pd.read_sql('SELECT * FROM v_ratios WHERE fiscal_year=?', c, params=(Y,))
rows = []
for _, x in r.iterrows():
    for s in [0, -0.1, -0.2, -0.3, -0.4]:
        lev = x.net_debt / (x.ebitda_model * (1 + s))
        rows.append({'issuer': x.issuer, 'shock': f'{s:.0%}', 'net_leverage': round(lev, 2), 'breach': lev > T})
res = pd.DataFrame(rows)
res.to_csv(f'outputs/stress_results_{Y}.csv', index=False)
print(Y)
print(res.pivot(index='shock', columns='issuer', values='net_leverage'))
r['breach_shock'] = (r.net_debt / (T * r.ebitda_model) - 1).round(3)
print(r[['issuer', 'net_leverage', 'breach_shock']])
