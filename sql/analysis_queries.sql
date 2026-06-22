USE rtc_db;

-- 1 Total Pages Per Report
SELECT
    report_name,
    COUNT(*) AS total_pages
FROM reports
GROUP BY report_name
ORDER BY total_pages DESC;

-- 2 Total Chunks Per Report
SELECT
    report_name,
    COUNT(*) AS total_chunks
FROM chunks
GROUP BY report_name
ORDER BY total_chunks DESC;

-- 3 Average Page Length
SELECT
    report_name,
    AVG(LENGTH(text_content)) AS avg_page_length
FROM reports
GROUP BY report_name
ORDER BY avg_page_length DESC;

-- 4 Longest Pages
SELECT
    report_name,
    page_number,
    LENGTH(text_content) AS page_length
FROM reports
ORDER BY page_length DESC
LIMIT 10;

-- 5 Metrics Count Per Report
SELECT
    report_name,
    COUNT(*) AS total_metrics
FROM metrics
GROUP BY report_name
ORDER BY total_metrics DESC;

-- 6 Business Metrics By Category
SELECT
    category,
    COUNT(*) AS total_metrics
FROM business_metrics
GROUP BY category
ORDER BY total_metrics DESC;

-- 7 Highest Business KPI Values
SELECT
    metric_name,
    metric_value
FROM business_metrics
ORDER BY metric_value DESC
LIMIT 10;

-- 8 Community Metrics
SELECT *
FROM business_metrics
WHERE category = 'Community';

-- 9 Career Metrics
SELECT *
FROM business_metrics
WHERE category = 'Career';

-- 10 Funding Metrics
SELECT *
FROM business_metrics
WHERE category = 'Funding';

-- 11 Event Metrics
SELECT *
FROM business_metrics
WHERE category = 'Events';

-- 12 Program Metrics
SELECT *
FROM business_metrics
WHERE category = 'Program';

-- 13 Average KPI By Year
SELECT
    year,
    AVG(metric_value) AS avg_metric_value
FROM business_metrics
GROUP BY year;

-- 14 KPI Distribution By Year
SELECT
    year,
    COUNT(*) AS total_kpis
FROM business_metrics
GROUP BY year;

-- 15 Top RTC Impact Indicators
SELECT
    metric_name,
    metric_value
FROM business_metrics
ORDER BY metric_value DESC;


SELECT COUNT(*) FROM business_metrics;