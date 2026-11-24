from bond_parser import parse

TESTS = [
    ('JSW STEEL 4.75% 2028 97.5/98.0', ('JSW Steel', 4.75, 2028, 97.5, 98.0)),
    ('TATA STEEL 6.0% 2031 102.00 / 102.50', ('Tata Steel', 6.0, 2031, 102.0, 102.5)),
    ('JSW STEEL 5.375 15/04/2028 97.8/98.3', ('JSW Steel', 5.375, 2028, 97.8, 98.3)),
    ('Jsw Steel 5.05% Mar-2029 98.75/99.25', ('JSW Steel', 5.05, 2029, 98.75, 99.25)),
    ('TATA STEEL 4.5% JUL 2027 99.5/100.0', ('Tata Steel', 4.5, 2027, 99.5, 100.0)),
    ('TATA STEEL 14.5% 2027 99.5/100.0 YLD 6.1', ('Tata Steel', 14.5, 2027, 99.5, 100.0)),
    ('JSW STEEL 5.05% 2029 98.75 - 99.25!!', ('JSW Steel', 5.05, 2029, 98.75, 99.25)),
    ('JSW STEEL 5.05% 2029 100.25/99.75', None),
    ('TATA STEEL 2027 99.5/100.0', None),
    ('WILL BUY TATA STEEL 4.5% 2027 AT 99.5', None),
    ('tata steel 4.5 2027 bid 99.5 offer 100.0', ('Tata Steel', 4.5, 2027, 99.5, 100.0)),
    ('JSW STEEL CALL 5.05% 2029 98/99', ('JSW Steel', 5.05, 2029, 98.0, 99.0)),
    ('5.05% JSW STEEL 2029 98.75/99.25', ('JSW Steel', 5.05, 2029, 98.75, 99.25)),
    ('TATA STEEL 4.5% 2027 99 1/2 / 100', ('Tata Steel', 4.5, 2027, 99.5, 100.0)),
]
F = ['issuer', 'coupon', 'maturity_year', 'bid', 'ask']
ok = 0
for msg, gold in TESTS:
    got = parse(msg)
    good = got is None if gold is None else (got is not None and all(got[f] == g for f, g in zip(F, gold)))
    ok += good
    if not good:
        print('FAIL:', msg, '->', got)
print(f'Extra set accuracy: {ok}/{len(TESTS)} = {ok / len(TESTS):.0%}')
