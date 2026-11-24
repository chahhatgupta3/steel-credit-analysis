# Tata Steel vs JSW Steel: FY25-FY26 Credit Comparison

Credit model built from consolidated filings, with data quality checks, an EBITDA stress test, SQL analysis and a bond quote parser.

- Net leverage FY25: Tata 3.18x, JSW 3.29x (company-reported 3.2x, 3.34x)
- Net leverage FY26: Tata 2.41x, JSW 1.77x (company-reported 2.3x, 1.81x)
- Data quality: automated checks caught a unit error (lakh vs crore) and mis-entered EBITDA
- Parser: OTC bond quote regex parser, 95% on a 22-message test set
- Tools: Python (pandas, pytest), SQLite, Excel

Rerun any year: python src/run_all.py FY26
See docs/PROCESS.md for definitions, data issues and limitations.
