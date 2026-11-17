import sqlite3, pandas as pd
from openpyxl import Workbook

w = pd.read_sql('SELECT * FROM v_wide', sqlite3.connect('db/credit.db')).set_index('issuer')
wb = Workbook()
ws = wb.active
ws.title = 'Inputs'
ws.append(['Item (INR crore)', 'Tata Steel', 'JSW Steel'])
for col in ['pbt', 'finance_costs', 'depreciation', 'exceptional_items', 'total_borrowings',
            'cash', 'other_bank', 'cur_inv', 'total_equity', 'ocf']:
    ws.append([col, float(w.loc['Tata Steel', col]), float(w.loc['JSW Steel', col])])

r = wb.create_sheet('Ratios')
r.append(['Metric', 'Tata Steel', 'JSW Steel'])
tmpl = [('Net debt', '=Inputs!{c}6-Inputs!{c}7-Inputs!{c}8-Inputs!{c}9'),
        ('EBITDA', '=Inputs!{c}2+Inputs!{c}3+Inputs!{c}4+Inputs!{c}5'),
        ('Net leverage (x)', '={c}2/{c}3'),
        ('Gearing (x)', '={c}2/Inputs!{c}10'),
        ('OCF / net debt', '=Inputs!{c}11/{c}2')]
for lab, t in tmpl:
    r.append([lab, t.format(c='B'), t.format(c='C')])

s = wb.create_sheet('Stress')
s.append(['EBITDA shock', 'Tata leverage', 'JSW leverage', 'Tata vs 4.5x', 'JSW vs 4.5x'])
for i, sh in enumerate([0, -0.1, -0.2, -0.3, -0.4], start=2):
    s.append([sh, f'=Ratios!$B$2/(Ratios!$B$3*(1+$A{i}))', f'=Ratios!$C$2/(Ratios!$C$3*(1+$A{i}))',
              f'=IF(B{i}>4.5,"BREACH","OK")', f'=IF(C{i}>4.5,"BREACH","OK")'])
    s[f'A{i}'].number_format = '0%'
s.append([])
s.append(['Breach point', '=Ratios!B2/(4.5*Ratios!B3)-1', '=Ratios!C2/(4.5*Ratios!C3)-1'])
s['B8'].number_format = '0.0%'
s['C8'].number_format = '0.0%'
wb.save('outputs/credit_model.xlsx')
print('saved')
