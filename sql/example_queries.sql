-- sql/example_queries.sql

SELECT d.*
FROM dams d
JOIN dam_group_members gm ON d.dam_id = gm.dam_id
WHERE gm.group_name = 'sydney_dams';

SELECT g.group_name
FROM dam_groups g
JOIN dam_group_members gm ON g.group_name = gm.group_name
WHERE gm.dam_id = '212232';

SELECT * FROM latest_data WHERE dam_id = '410102';

SELECT * FROM dam_resources WHERE dam_id = '42510037' ORDER BY date;

SELECT * FROM specific_dam_analysis
WHERE dam_id = '210097' AND analysis_date = '2024-11-01';

SELECT * FROM overall_dam_analysis
WHERE analysis_date = '2024-11-25';
