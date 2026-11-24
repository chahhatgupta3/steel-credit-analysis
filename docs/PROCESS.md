# Credit Comparison: Tata Steel vs JSW Steel (FY25)

## Purpose
Compare leverage, gearing and cash-flow cover for two Indian steel issuers from consolidated FY25 filings, stress-test EBITDA, and parse dealer-style bond quotes.

## How to rerun
python src/build_db.py && python src/checks.py && python src/stress.py && python src/build_excel.py && pytest -v

## Definitions
- Net debt = total borrowings - cash - other bank balances - current investments
- EBITDA (model) = PBT + finance costs + depreciation + exceptional items
- Net leverage = net debt / EBITDA; Gearing = net debt / total equity; OCF/net debt = OCF / net debt
- Breach threshold = 4.5x net leverage. Stress holds net debt constant.

## Sources
Tata Steel Integrated Report FY25 and Q4 FY25 consolidated filing; JSW Steel Integrated Annual Report FY25 (pages in inputs/financials.csv).

## Data issues found and fixed
1. EBITDA entered wrongly for both issuers (Tata: copied PBT; JSW: single-quarter figure). Caught by the EBITDA recompute check, corrected from annual reports.
2. Tata total borrowings missed current borrowings (21,416.53). Fixed; net leverage then reconciled to company-reported 3.2x.
3. JSW inputs were standalone, not consolidated (revenue, balance sheet, OCF). Replaced with consolidated figures; net leverage then reconciled to company-reported 3.34x.
4. SQLite integer division returned 0 for ratios. Fixed by storing values as floats.

## Known limitations
- JSW gross debt is derived: reported net debt (76,563) + cash (19,394). Other bank balances and current investments set to 0 for JSW.
- Tata lease liabilities not added separately (model reconciles to company figure without them).
- JSW model EBITDA differs from company operating EBITDA by about 2% (definition difference).
- Stress test holds net debt constant, a simplification.
- Parser test set is small (9 clean, 8 hard messages).

## Results
- Net leverage: Tata 3.18x, JSW 3.29x (company-reported: 3.2x, 3.34x)
- Breach of 4.5x at EBITDA fall of 29.3% (Tata) and 26.9% (JSW); both breach at -30%
- Data quality checks: 14/14 passing after fixes (12/14 on first run)
- Parser: hard set 50% -> 100% after four regex fixes
- UAT: 8/8 pytest tests passing

## FY26 update
- FY26 added; tooling runs for any year with: python src/run_all.py FY26
- Tata FY26 filing was in INR lakh; converted to crore (/100), noted in the CSV
- JSW FY26 reported EBITDA corrected to operating EBITDA (29,821) after the EBITDA check failed
- Tata net debt: model 81,321 vs company 80,144. Gap = FX hedges against borrowings and non-current earmarked bank balances, which the model excludes (same pattern in FY25: 282). Lease obligations are already inside balance sheet borrowings.
- Tata net leverage 2.41x vs company-reported 2.3x (model EBITDA is built from PBT, about 3% below reported)
- JSW net leverage 1.77x vs company-reported 1.81x
