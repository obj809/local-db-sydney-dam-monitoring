
SHOW DATABASES;

USE dam_monitoring_db;


SELECT * FROM dams LIMIT 10;
SELECT * FROM latest_data LIMIT 10;
SELECT * FROM dam_resources LIMIT 10;
SELECT * FROM specific_dam_analysis LIMIT 10;
SELECT * FROM overall_dam_analysis LIMIT 10;
SELECT * FROM dam_groups LIMIT 10;
SELECT * FROM dam_group_members LIMIT 10;


-- Join Tables to Analyze Relationships: Find all dams and their latest data
SELECT 
    d.dam_id, 
    d.dam_name, 
    d.full_volume, 
    l.date, 
    l.storage_volume, 
    l.percentage_full
FROM dams d
JOIN latest_data l ON d.dam_id = l.dam_id;

SELECT 
    dg.group_name,
    GROUP_CONCAT(d.dam_name ORDER BY d.dam_name SEPARATOR ', ') AS members
FROM 
    dam_groups dg
LEFT JOIN 
    dam_group_members gm ON dg.group_name = gm.group_name
LEFT JOIN 
    dams d ON gm.dam_id = d.dam_id
GROUP BY 
    dg.group_name
ORDER BY 
    dg.group_name;