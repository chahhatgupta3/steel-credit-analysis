-- SETUP: issuer reference table
CREATE TABLE IF NOT EXISTS issuers (issuer TEXT PRIMARY KEY, sector TEXT, country TEXT);
INSERT OR IGNORE INTO issuers VALUES ('Tata Steel', 'Steel', 'India'), ('JSW Steel', 'Steel', 'India');

-- 1. JOIN: ratios with issuer details
SELECT r.issuer, i.sector, i.country, r.fiscal_year, r.net_leverage, r.gearing
FROM v_ratios r JOIN issuers i ON i.issuer = r.issuer;

-- 2. WINDOW FUNCTIONS: rank per year, change vs prior year
SELECT issuer, fiscal_year, net_leverage,
  RANK() OVER (PARTITION BY fiscal_year ORDER BY net_leverage) AS rank_lowest_best,
  ROUND(net_leverage - LAG(net_leverage) OVER (PARTITION BY issuer ORDER BY fiscal_year), 2) AS change_vs_prior_year
FROM v_ratios;

-- 3. SUBQUERY: issuers with leverage above the average
SELECT issuer, fiscal_year, net_leverage
FROM v_ratios
WHERE net_leverage > (SELECT AVG(net_leverage) FROM v_ratios);

-- 4. CTE: headroom before breaching 4.5x
WITH h AS (
  SELECT issuer, fiscal_year, ROUND(net_debt / (4.5 * ebitda_model) - 1, 3) AS breach_shock
  FROM v_ratios)
SELECT * FROM h ORDER BY breach_shock DESC;

-- 5. DATA QUALITY: inputs missing a source
SELECT issuer, fiscal_year, line_item FROM financials
WHERE source_doc IS NULL OR source_doc = '' OR page_no IS NULL;
