import sqlite3, pandas as pd

c = sqlite3.connect('db/credit.db')
for s in open('docs/queries.sql').read().split(';'):
    lines = s.strip().split('\n')
    title = [l for l in lines if l.startswith('--')]
    body = '\n'.join(l for l in lines if not l.startswith('--')).strip()
    if not body:
        continue
    if body.upper().startswith(('SELECT', 'WITH')):
        print('\n' + (title[0] if title else ''))
        print(pd.read_sql(body, c).to_string(index=False))
    else:
        c.execute(body)
c.commit()
