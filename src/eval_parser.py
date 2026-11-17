from bond_parser import parse

TESTS = [
    ('TATA STEEL 4.5% 2027 99.5/100.0', ('Tata Steel', 4.5, 2027, 99.5, 100.0)),
    ('JSW STEEL 5.05 04/2027 98.75 / 99.25', ('JSW Steel', 5.05, 2027, 98.75, 99.25)),
    ('TATASTEEL 4.50 15-Jul-27 99.5/100', ('Tata Steel', 4.5, 2027, 99.5, 100.0)),
    ('JSW STEEL 3.95% 2029 96.10-96.60', ('JSW Steel', 3.95, 2029, 96.1, 96.6)),
    ('tata steel 5.5 2030 101.25 / 101.75', ('Tata Steel', 5.5, 2030, 101.25, 101.75)),
    ('TATA STEEL 4.5% 2027 100.5/99.5', None),
    ('TATA STEEL BIDS WANTED', None),
    ('NO QUOTE TODAY', None),
    ('SAIL 4.0% 2028 98/99', None),
]
F = ['issuer', 'coupon', 'maturity_year', 'bid', 'ask']
ok = 0
for msg, gold in TESTS:
    got = parse(msg)
    if gold is None:
        good = got is None
    else:
        good = got is not None and all(got[f] == g for f, g in zip(F, gold))
    ok += good
    if not good:
        print('FAIL:', msg, '->', got)
print(f'Accuracy: {ok}/{len(TESTS)} = {ok / len(TESTS):.0%}')
