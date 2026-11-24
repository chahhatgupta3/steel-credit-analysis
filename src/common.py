import sys, pandas as pd

def get_year(conn):
    if len(sys.argv) > 1:
        return sys.argv[1]
    return pd.read_sql('SELECT MAX(fiscal_year) AS y FROM financials', conn).y[0]
