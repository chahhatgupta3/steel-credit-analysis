import re

ISS = '(?P<issuer>[A-Z][A-Z &.]*?)'
CPN = '(?P<coupon>[0-9]+(?:[.][0-9]+)?)'
MAT = ('(?P<maturity>[0-9]{1,2}[-/ ][A-Za-z0-9]{2,3}[-/ ][0-9]{2,4}'
       '|[A-Za-z]{3}[-/ ][0-9]{2,4}|[0-9]{2}/[0-9]{4}|[0-9]{4})')
PX = ('(?:BID|B)?[ ]*(?P<bid>[0-9]{2,3}(?:[.][0-9]+)?)[ ]*'
      '(?:[/@-]|OFFER[ ]*|O[ ]*)[ ]*(?P<ask>[0-9]{2,3}(?:[.][0-9]+)?)')

P1 = re.compile(ISS + '[ ]+' + CPN + '[ ]*%?[ ]+' + MAT + '[ ]+' + PX)
P2 = re.compile(CPN + '[ ]*%?[ ]+' + ISS + '[ ]+' + MAT + '[ ]+' + PX)

ALIASES = {'TATA STEEL': 'Tata Steel', 'TATASTEEL': 'Tata Steel', 'TATA STL': 'Tata Steel',
           'JSW STEEL': 'JSW Steel', 'JSWSTEEL': 'JSW Steel', 'JSW STL': 'JSW Steel'}

def maturity_year(m):
    tail = re.search('([0-9]+)$', m).group(1)
    return int(tail) if len(tail) == 4 else 2000 + int(tail)

def parse(msg):
    text = msg.upper().strip()
    m = P1.search(text) or P2.search(text)
    if not m:
        return None
    name = m.group('issuer').strip()
    issuer = next((v for k, v in ALIASES.items() if k in name), None)
    bid, ask = float(m.group('bid')), float(m.group('ask'))
    if issuer is None or bid > ask:
        return None
    return {'issuer': issuer, 'coupon': float(m.group('coupon')),
            'maturity_year': maturity_year(m.group('maturity')), 'bid': bid, 'ask': ask}
