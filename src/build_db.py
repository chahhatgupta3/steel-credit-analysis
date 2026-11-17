import sqlite3, pandas as pd

df = pd.read_csv('inputs/financials.csv'); df['value_inr_cr'] = df['value_inr_cr'].astype(float)
conn = sqlite3.connect('db/credit.db')
conn.executescript('DROP VIEW IF EXISTS v_ratios; DROP VIEW IF EXISTS v_wide; DROP TABLE IF EXISTS financials;')
df.to_sql('financials', conn, index=False)

cols = {'revenue': 'revenue', 'pbt': 'pbt', 'finance_costs': 'finance_costs',
        'depreciation': 'depreciation', 'exceptional_items': 'exceptional_items',
        'ebitda_reported': 'ebitda_reported', 'total_borrowings': 'total_borrowings',
        'cash_and_cash_equivalents': 'cash', 'other_bank_balances': 'other_bank',
        'current_investments': 'cur_inv', 'total_equity': 'total_equity',
        'total_assets': 'total_assets', 'ocf': 'ocf'}
sel = ', '.join(f"MAX(CASE WHEN line_item='{k}' THEN value_inr_cr END) AS {v}" for k, v in cols.items())
conn.executescript(f'CREATE VIEW v_wide AS SELECT issuer, fiscal_year, {sel} FROM financials GROUP BY issuer, fiscal_year;')

nd = 'total_borrowings - cash - other_bank - cur_inv'
eb = 'pbt + finance_costs + depreciation + exceptional_items'
conn.executescript(f'''CREATE VIEW v_ratios AS SELECT issuer, fiscal_year,
  {nd} AS net_debt, {eb} AS ebitda_model,
  ROUND(({nd})/({eb}),2) AS net_leverage,
  ROUND(({nd})/total_equity,2) AS gearing,
  ROUND(ocf/({nd}),3) AS ocf_to_net_debt FROM v_wide;''')
conn.commit()
pd.set_option('display.width', 200)
print(pd.read_sql('SELECT * FROM v_ratios', conn))
