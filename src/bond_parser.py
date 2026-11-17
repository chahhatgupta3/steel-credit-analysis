import re

PATTERN = re.compile(
    '(?P<issuer>[A-Z][A-Z &.]*?)[ ]+'
    '(?P<coupon>[0-9]+(?:[.][0-9]+)?)[ ]*%?[ ]+'
    '(?P<maturity>[0-9]{1,2}[-/ ][A-Za-z0-9]{2,3}[-/ ][0-9]{2,4}|[A-Za-z]{3}[-/ ][0-9]{2,4}|[0-9]{2}/[0-9]{4}|[0-9]{4})[ ]+'
    '(?:B[ ]*)?(?P<bid>[0-9]{2,3}(?:[.][0-9]+)?)[ ]*(?:[/@-]|O[ ]*)[ ]*(?P<ask>[0-9]{2,3}(?:[.][0-9]+)?)'
)
ALIASES = {'TATA STEEL': 'Tata Steel', 'TATASTEEL': 'Tata Steel', 'TATA STL': 'Tata Steel',
           'JSW STEEL': 'JSW Steel', 'JSWSTEEL': 'JSW Steel', 'JSW STL': 'JSW Steel'}

def maturity_year(m):
    tail = re.search('([0-9]+)$', m).group(1)
    return int(tail) if len(tail) == 4 else 2000 + int(tail)

def parse(msg):
    m = PATTERN.search(msg.upper().strip())
    if not m:
        return None
    issuer = ALIASES.get(m.group('issuer').strip())
    bid, ask = float(m.group('bid')), float(m.group('ask'))
    if issuer is None or bid > ask:
        return None
    return {'issuer': issuer, 'coupon': float(m.group('coupon')),
            'maturity_year': maturity_year(m.group('maturity')), 'bid': bid, 'ask': ask}
