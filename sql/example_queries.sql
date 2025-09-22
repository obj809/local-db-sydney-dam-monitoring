-- sql/example_queries.sql

SET @today = CURDATE();
SET @start_24m = DATE_SUB(@today, INTERVAL 24 MONTH);
SET @start_12m = DATE_SUB(@today, INTERVAL 12 MONTH);
SET @last_month_end = LAST_DAY(DATE_SUB(@today, INTERVAL 1 MONTH));


SELECT COUNT(*) AS dam_count FROM dams;

SELECT d.dam_id, d.dam_name
FROM dams d
LEFT JOIN latest_data ld ON ld.dam_id = d.dam_id
WHERE ld.dam_id IS NULL
ORDER BY d.dam_id;

SELECT d.dam_id, d.dam_name
FROM dams d
LEFT JOIN dam_resources r
  ON r.dam_id = d.dam_id
 AND r.date >= @start_24m
WHERE r.dam_id IS NULL
ORDER BY d.dam_id;


SELECT g.group_name, COUNT(m.dam_id) AS member_count
FROM dam_groups g
LEFT JOIN dam_group_members m ON m.group_name = g.group_name
GROUP BY g.group_name
ORDER BY g.group_name;

SELECT m.group_name, d.dam_id, d.dam_name
FROM dam_group_members m
JOIN dams d ON d.dam_id = m.dam_id
WHERE m.group_name = 'sydney_dams'
ORDER BY d.dam_id;

SELECT m.dam_id, m.group_name
FROM dam_group_members m
WHERE m.dam_id = '212232'
ORDER BY m.group_name;


SELECT
  ld.dam_id,
  ld.dam_name,
  ld.date,
  DATEDIFF(@today, ld.date) AS days_old,
  ld.storage_volume,
  ld.percentage_full,
  ld.storage_inflow,
  ld.storage_release
FROM latest_data ld
ORDER BY ld.date DESC, ld.dam_id;

SELECT
  (SELECT COUNT(*) FROM dams) AS dams_count,
  (SELECT COUNT(*) FROM latest_data) AS latest_data_rows;

SELECT d.dam_id, d.dam_name, COUNT(r.resource_id) AS rows_24m
FROM dams d
LEFT JOIN dam_resources r
  ON r.dam_id = d.dam_id
 AND r.date >= @start_24m
GROUP BY d.dam_id, d.dam_name
ORDER BY d.dam_id;

SELECT r.*
FROM dam_resources r
WHERE r.dam_id = '212243'
ORDER BY r.date DESC;

SELECT
  d.dam_id,
  d.dam_name,
  ROUND(AVG(r.percentage_full), 2) AS avg_pct_full_12m,
  MIN(r.date) AS first_date_in_window,
  MAX(r.date) AS last_date_in_window
FROM dams d
JOIN dam_resources r
  ON r.dam_id = d.dam_id
WHERE r.date >= @start_12m
GROUP BY d.dam_id, d.dam_name
ORDER BY avg_pct_full_12m DESC;

WITH last_resource AS (
  SELECT r.dam_id, r.percentage_full, r.date
  FROM dam_resources r
  JOIN (
    SELECT dam_id, MAX(date) AS max_date
    FROM dam_resources
    GROUP BY dam_id
  ) mx ON mx.dam_id = r.dam_id AND mx.max_date = r.date
)
SELECT
  d.dam_id,
  d.dam_name,
  ld.date AS latest_date,
  ld.percentage_full AS latest_pct,
  lr.date AS last_resource_date,
  lr.percentage_full AS resource_pct,
  ROUND(ld.percentage_full - lr.percentage_full, 2) AS pct_diff
FROM dams d
LEFT JOIN latest_data ld ON ld.dam_id = d.dam_id
LEFT JOIN last_resource lr ON lr.dam_id = d.dam_id
ORDER BY d.dam_id;

SELECT
  s.dam_id,
  MAX(s.analysis_date) AS latest_analysis_date
FROM specific_dam_analysis s
GROUP BY s.dam_id
ORDER BY s.dam_id;

SELECT s.*
FROM specific_dam_analysis s
JOIN (
  SELECT dam_id, MAX(analysis_date) AS latest_date
  FROM specific_dam_analysis
  WHERE dam_id = '210097'
) mx ON mx.dam_id = s.dam_id AND mx.latest_date = s.analysis_date;

SELECT *
FROM specific_dam_analysis
WHERE analysis_date = @last_month_end
ORDER BY dam_id;

SELECT *
FROM overall_dam_analysis
ORDER BY analysis_date DESC
LIMIT 6;

SELECT ld.dam_id
FROM latest_data ld
LEFT JOIN dams d ON d.dam_id = ld.dam_id
WHERE d.dam_id IS NULL;

SELECT DISTINCT r.dam_id
FROM dam_resources r
LEFT JOIN dams d ON d.dam_id = r.dam_id
WHERE d.dam_id IS NULL;

SELECT *
FROM dam_group_members m
LEFT JOIN dams d ON d.dam_id = m.dam_id
LEFT JOIN dam_groups g ON g.group_name = m.group_name
WHERE d.dam_id IS NULL OR g.group_name IS NULL;
