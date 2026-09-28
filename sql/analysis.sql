-- SQLite 3.25+; source amounts are thousands of Canadian dollars.
-- Use year-over-year comparisons for unadjusted monthly data.

-- QUERY: Latest month: Edmonton versus Calgary and Alberta
SELECT month, geography,
       ROUND(sales_cad_thousands / 1000000.0, 3) AS sales_cad_billions,
       quality_status
FROM retail_sales
WHERE month = (SELECT MAX(month) FROM retail_sales)
ORDER BY CASE geography WHEN 'Edmonton, Alberta' THEN 1 WHEN 'Calgary, Alberta' THEN 2
                        WHEN 'Alberta' THEN 3 ELSE 4 END;

-- QUERY: Year-over-year change for Edmonton and Calgary, latest month
WITH growth AS (
    SELECT month, geography, sales_cad_thousands,
           LAG(sales_cad_thousands, 12) OVER (PARTITION BY geography ORDER BY month) AS prior_year
    FROM retail_sales
)
SELECT month, geography,
       ROUND(100.0 * (sales_cad_thousands - prior_year) / NULLIF(prior_year, 0), 2) AS yoy_pct
FROM growth
WHERE month = (SELECT MAX(month) FROM retail_sales)
  AND geography IN ('Edmonton, Alberta', 'Calgary, Alberta')
ORDER BY geography DESC;

-- QUERY: Edmonton share of Alberta retail sales, latest month
SELECT e.month,
       ROUND(100.0 * e.sales_cad_thousands / NULLIF(a.sales_cad_thousands, 0), 2) AS edmonton_share_pct
FROM retail_sales AS e
JOIN retail_sales AS a ON e.month = a.month
WHERE e.geography = 'Edmonton, Alberta' AND a.geography = 'Alberta'
  AND e.month = (SELECT MAX(month) FROM retail_sales);

-- QUERY: Year-over-year trend for Edmonton (most recent 12 months)
WITH growth AS (
    SELECT month, geography, sales_cad_thousands,
           LAG(sales_cad_thousands, 12) OVER (PARTITION BY geography ORDER BY month) AS prior_year
    FROM retail_sales
)
SELECT month, ROUND(sales_cad_thousands / 1000000.0, 3) AS sales_cad_billions,
       ROUND(100.0 * (sales_cad_thousands - prior_year) / NULLIF(prior_year, 0), 2) AS yoy_pct
FROM growth
WHERE geography = 'Edmonton, Alberta' AND prior_year IS NOT NULL
ORDER BY month DESC LIMIT 12;
