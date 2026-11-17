import sqlite3, sys
import pytest
sys.path.insert(0, 'src')
from bond_parser import parse

conn = sqlite3.connect('db/credit.db')

def ratio(issuer, col):
    return conn.execute(f'SELECT {col} FROM v_ratios WHERE issuer=?', (issuer,)).fetchone()[0]

def test_tata_net_leverage():
    assert ratio('Tata Steel', 'net_leverage') == pytest.approx(3.18, abs=0.01)

def test_jsw_net_leverage():
    assert ratio('JSW Steel', 'net_leverage') == pytest.approx(3.29, abs=0.01)

def test_tata_net_debt():
    assert ratio('Tata Steel', 'net_debt') == pytest.approx(82712, abs=1)

def test_breach_point_formula():
    nd, e = ratio('Tata Steel', 'net_debt'), ratio('Tata Steel', 'ebitda_model')
    s = nd / (4.5 * e) - 1
    assert nd / (e * (1 + s)) == pytest.approx(4.5)

def test_parser_basic():
    assert parse('TATA STEEL 4.5% 2027 99.5/100.0')['ask'] == 100.0

def test_parser_bid_offer_format():
    assert parse('TATA STEEL 4.5% 2027 B 99.5 O 100.0')['bid'] == 99.5

def test_parser_crossed_market_rejected():
    assert parse('TATA STEEL 4.5% 2027 100.5/99.5') is None

def test_parser_non_quote_rejected():
    assert parse('PLS SEND LEVELS') is None
