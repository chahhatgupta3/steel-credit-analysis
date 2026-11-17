from bond_parser import parse

TESTS = [
    ('TATA STEEL 4.5% 2027 99.5/100.0 SIZE 5MM', ('Tata Steel', 4.5, 2027, 99.5, 100.0)),
    ('RE: TATA STEEL 4.5% 2027 99.5/100.0', ('Tata Steel', 4.5, 2027, 99.5, 100.0)),
    ('TATA STEEL 4.5% 2027 B 99.5 O 100.0', ('Tata Steel', 4.5, 2027, 99.5, 100.0)),
    ('JSW STEEL 5.05% MAR-27 98.75/99.25', ('JSW Steel', 5.05, 2027, 98.75, 99.25)),
    ('JSW STEEL 5.05 2029 98.75@99.25', ('JSW Steel', 5.05, 2029, 98.75, 99.25)),
    ('TATA STL 4.5% 2027 99.5/100.0', ('Tata Steel', 4.5, 2027, 99.5, 100.0)),
    ('JSW STEEL 4.75 05/2027 YLD 6.1', None),
    ('PLS SEND LEVELS', None),
]
F = ['issuer', 'coupon', 'maturity_year', 'bid', 'ask']
ok = 0
for msg, gold in TESTS:
    got = parse(msg)
    good = got is None if gold is None else (got is not None and all(got[f] == g for f, g in zip(F, gold)))
    ok += good
    if not good:
        print('FAIL:', msg, '->', got)
print(f'Hard set accuracy: {ok}/{len(TESTS)} = {ok / len(TESTS):.0%}')
