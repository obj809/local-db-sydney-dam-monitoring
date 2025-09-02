-- sql/example_data.sql


INSERT INTO dams (dam_id, dam_name, full_volume, latitude, longitude) VALUES
    ('203042', 'Toonumbar Dam', 10814, -28.602383, 152.763769),
    ('210097', 'Glenbawn Dam', 748827, -32.064304, 150.982007),
    ('210102', 'Lostock Dam', 19736, -32.335999, 151.440793),
    ('210117', 'Glennies Creek Dam', 282303, -32.339259, 151.286947),
    ('212205', 'Nepean Dam', 67730, -34.335046, 150.617666),
    ('212211', 'Avon Dam', 142230, -34.350932, 150.6405),
    ('212212', 'Wingecarribee Reservoir', 29880, -34.540413, 150.498916),
    ('212220', 'Cordeaux Dam', 93790, -34.336403, 150.745918),
    ('212232', 'Cataract Dam', 97190, -34.265584, 150.803553),
    ('212243', 'Warragamba Dam', 2064680, -33.891111, 150.591111),
    ('213210', 'Woronora Dam', 69536, -34.109296, 150.936519),
    ('213240', 'Prospect Reservoir', 33330, -33.832851, 150.890158),
    ('215212', 'Tallowa Dam', 7500, -34.771563, 150.315266),
    ('215235', 'Fitzroy Falls Reservoir', 9950, -34.645106, 150.48719),
    ('219027', 'Brogo Dam', 8786, -36.476593, 149.722275),
    ('219033', 'Cochrane Dam', 2700, -36.5703, 149.4554),
    ('410102', 'Blowering Dam', 1604010, -35.515836, 148.254929),
    ('410131', 'Burrinjuck Dam', 1024750, -35.014067, 148.643656),
    ('412010', 'Lake Wyangala', 1217035, -33.931625, 149.010236),
    ('412106', 'Carcoar Dam', 35917, -33.601561, 149.203153),
    ('412107', 'Lake Cargelligo', 30163, -33.295281, 146.390692),
    ('412108', 'Lake Brewster', 145369, -33.492387, 145.975896),
    ('416030', 'Pindari Dam', 311500, -29.381739, 151.269225),
    ('418035', 'Copeton Dam', 1345510, -29.904891, 150.989479),
    ('419041', 'Keepit Dam', 418950, -30.819471, 150.516625),
    ('419069', 'Chaffey Dam', 100509, -31.356884, 151.119117),
    ('419080', 'Split Rock Dam', 393840, -30.537122, 150.674591),
    ('421078', 'Burrendong Dam', 1154270, -32.688321, 149.157884),
    ('421148', 'Windamere Dam', 366989, -32.782606, 149.81548),
    ('421189', 'Oberon Dam', 45000, -33.72467, 149.866781),
    ('425022', 'Lake Menindee', 629492, -32.343792, 142.328445),
    ('425023', 'Lake Cawndilla', 631050, -32.475672, 142.229739),
    ('425046', 'Lake Wetherell', 115759, -32.311286, 142.54764),
    ('425047', 'Lake Tandure', 77419, -32.27323, 142.5424),
    ('42510036', 'Lake Pamamaroo', 270001, -32.3, 142.44),
    ('42510037', 'Lake Copi Hollow', 7729, -32.254265, 142.392175);


INSERT INTO dam_groups (group_name) VALUES
    ('sydney_dams'),
    ('popular_dams'),
    ('large_dams'),
    ('small_dams'),
    ('greatest_released');


-- Sydney Dams
INSERT INTO dam_group_members (group_name, dam_id) VALUES
    ('sydney_dams', '212232'),
    ('sydney_dams', '212220'),
    ('sydney_dams', '212211'),
    ('sydney_dams', '212205'),
    ('sydney_dams', '213210'),
    ('sydney_dams', '213240'),
    ('sydney_dams', '212212'),
    ('sydney_dams', '215235');

-- Popular Dams
INSERT INTO dam_group_members (group_name, dam_id) VALUES
    ('popular_dams', '212243'),
    ('popular_dams', '212232'),
    ('popular_dams', '212220'),
    ('popular_dams', '212211'),
    ('popular_dams', '212205'),
    ('popular_dams', '213210'),
    ('popular_dams', '215212'),
    ('popular_dams', '213240');

-- Large Dams
INSERT INTO dam_group_members (group_name, dam_id) VALUES
    ('large_dams', '212243'),
    ('large_dams', '410102'),
    ('large_dams', '412010'),
    ('large_dams', '418035'),
    ('large_dams', '410131'),
    ('large_dams', '421078'),
    ('large_dams', '210097'),
    ('large_dams', '419080');

-- Small Dams
INSERT INTO dam_group_members (group_name, dam_id) VALUES
    ('small_dams', '219033'),
    ('small_dams', '215235'),
    ('small_dams', '215212'),
    ('small_dams', '42510037'),
    ('small_dams', '219027'),
    ('small_dams', '203042'),
    ('small_dams', '210102'),
    ('small_dams', '412107');

-- Greatest Released Dams
INSERT INTO dam_group_members (group_name, dam_id) VALUES
    ('greatest_released', '410102'),
    ('greatest_released', '410131'),
    ('greatest_released', '421078'),
    ('greatest_released', '418035'),
    ('greatest_released', '210117'),
    ('greatest_released', '210097'),
    ('greatest_released', '419041'),
    ('greatest_released', '412010');


INSERT INTO latest_data (dam_id, dam_name, date, storage_volume, percentage_full, storage_inflow, storage_release) VALUES
    ('203042', 'Toonumbar Dam', '2024-11-25', 10500.000, 97.00, 500.500, 300.300),
    ('210097', 'Glenbawn Dam', '2024-11-25', 730000.000, 97.45, 2200.200, 1600.000),
    ('210102', 'Lostock Dam', '2024-11-25', 19500.000, 98.77, 600.000, 350.800),
    ('210117', 'Glennies Creek Dam', '2024-11-25', 280000.000, 99.50, 1800.500, 1300.300),
    ('212205', 'Nepean Dam', '2024-11-25', 68000.000, 95.00, 1180.700, 790.400),
    ('212211', 'Avon Dam', '2024-11-25', 140000.000, 98.00, 1150.600, 770.500),
    ('212212', 'Wingecarribee Reservoir', '2024-11-25', 29500.000, 99.00, 1050.200, 730.000),
    ('212220', 'Cordeaux Dam', '2024-11-25', 93000.000, 99.20, 1400.000, 800.000),
    ('212232', 'Cataract Dam', '2024-11-25', 96000.000, 98.90, 1500.500, 820.300),
    ('212243', 'Warragamba Dam', '2024-11-25', 2064000.000, 100.00, 2500.700, 1800.600),
    ('213210', 'Woronora Dam', '2024-11-25', 69000.000, 99.50, 1250.900, 820.100),
    ('213240', 'Prospect Reservoir', '2024-11-25', 33000.000, 99.50, 800.300, 600.700),
    ('215212', 'Tallowa Dam', '2024-11-25', 7400.000, 99.33, 700.000, 400.300),
    ('215235', 'Fitzroy Falls Reservoir', '2024-11-25', 9900.000, 100.00, 800.600, 500.400),
    ('219027', 'Brogo Dam', '2024-11-25', 8700.000, 99.00, 550.800, 330.600),
    ('219033', 'Cochrane Dam', '2024-11-25', 2700.000, 100.00, 580.900, 340.700),
    ('410102', 'Blowering Dam', '2024-11-25', 1603000.000, 99.90, 2000.500, 1500.300),
    ('410131', 'Burrinjuck Dam', '2024-11-25', 1024000.000, 99.90, 2050.800, 1520.300),
    ('412010', 'Lake Wyangala', '2024-11-25', 1217000.000, 99.80, 2100.600, 1550.500),
    ('412106', 'Carcoar Dam', '2024-11-25', 36000.000, 99.90, 400.300, 250.700),
    ('412107', 'Lake Cargelligo', '2024-11-25', 30000.000, 99.80, 620.100, 360.900),
    ('412108', 'Lake Brewster', '2024-11-25', 145300.000, 99.90, 700.000, 500.500),
    ('416030', 'Pindari Dam', '2024-11-25', 310000.000, 99.50, 900.000, 600.300),
    ('418035', 'Copeton Dam', '2024-11-25', 1345000.000, 99.80, 1900.700, 1450.400),
    ('419041', 'Keepit Dam', '2024-11-25', 420000.000, 99.90, 1850.600, 1350.400),
    ('419069', 'Chaffey Dam', '2024-11-25', 100500.000, 99.90, 950.000, 550.400),
    ('419080', 'Split Rock Dam', '2024-11-25', 394000.000, 99.80, 2250.300, 1620.100),
    ('421078', 'Burrendong Dam', '2024-11-25', 1154000.000, 99.80, 1950.900, 1480.100),
    ('421148', 'Windamere Dam', '2024-11-25', 367000.000, 99.90, 1600.200, 1100.700),
    ('421189', 'Oberon Dam', '2024-11-25', 45000.000, 99.90, 800.300, 500.700),
    ('425022', 'Lake Menindee', '2024-11-25', 630000.000, 99.80, 1800.500, 1200.300),
    ('425023', 'Lake Cawndilla', '2024-11-25', 630000.000, 99.90, 1750.500, 1150.300),
    ('425046', 'Lake Wetherell', '2024-11-25', 115700.000, 99.90, 600.300, 350.200),
    ('425047', 'Lake Tandure', '2024-11-25', 77000.000, 99.90, 650.300, 400.200),
    ('42510036', 'Lake Pamamaroo', '2024-11-25', 270000.000, 100.00, 750.000, 450.000),
    ('42510037', 'Lake Copi Hollow', '2024-11-25', 7700.000, 99.90, 700.000, 400.200);


-- Toonumbar Dam (203042)
INSERT INTO dam_resources (dam_id, date, storage_volume, percentage_full, storage_inflow, storage_release) VALUES
    ('203042', '2023-10-01', 10500.000, 95.00, 480.500, 300.300),
    ('203042', '2023-11-01', 10600.000, 96.00, 500.500, 310.300),
    ('203042', '2023-12-01', 10700.000, 97.00, 520.500, 320.300);

-- Glenbawn Dam (210097)
INSERT INTO dam_resources (dam_id, date, storage_volume, percentage_full, storage_inflow, storage_release) VALUES
    ('210097', '2023-10-01', 740000.000, 95.00, 2200.200, 1500.000),
    ('210097', '2023-11-01', 745000.000, 96.00, 2250.200, 1550.000),
    ('210097', '2023-12-01', 750000.000, 97.00, 2300.200, 1600.000);

-- Lostock Dam (210102)
INSERT INTO dam_resources (dam_id, date, storage_volume, percentage_full, storage_inflow, storage_release) VALUES
    ('210102', '2023-10-01', 19500.000, 96.00, 600.000, 350.800),
    ('210102', '2023-11-01', 19800.000, 97.00, 610.000, 360.800),
    ('210102', '2023-12-01', 20000.000, 98.00, 620.000, 370.800);

-- Warragamba Dam (212243)
INSERT INTO dam_resources (dam_id, date, storage_volume, percentage_full, storage_inflow, storage_release) VALUES
    ('212243', '2023-10-01', 2064000.000, 98.00, 2500.700, 1800.600),
    ('212243', '2023-11-01', 2065000.000, 99.00, 2520.700, 1850.600),
    ('212243', '2023-12-01', 2064680.000, 100.00, 2550.700, 1900.600);

-- Blowering Dam (410102)
INSERT INTO dam_resources (dam_id, date, storage_volume, percentage_full, storage_inflow, storage_release) VALUES
    ('410102', '2023-10-01', 1600000.000, 98.00, 2000.500, 1500.300),
    ('410102', '2023-11-01', 1602000.000, 98.50, 2010.500, 1510.300),
    ('410102', '2023-12-01', 1604010.000, 99.00, 2020.500, 1520.300);

-- Burrinjuck Dam (410131)
INSERT INTO dam_resources (dam_id, date, storage_volume, percentage_full, storage_inflow, storage_release) VALUES
    ('410131', '2023-10-01', 1024000.000, 98.00, 2050.800, 1520.300),
    ('410131', '2023-11-01', 1025000.000, 98.50, 2060.800, 1530.300),
    ('410131', '2023-12-01', 1024750.000, 99.00, 2070.800, 1540.300);

-- Lake Wyangala (412010)
INSERT INTO dam_resources (dam_id, date, storage_volume, percentage_full, storage_inflow, storage_release) VALUES
    ('412010', '2023-10-01', 1217000.000, 98.00, 2100.600, 1550.500),
    ('412010', '2023-11-01', 1218000.000, 98.50, 2110.600, 1560.500),
    ('412010', '2023-12-01', 1217035.000, 99.00, 2120.600, 1570.500);

-- Copeham Dam (42510037)
INSERT INTO dam_resources (dam_id, date, storage_volume, percentage_full, storage_inflow, storage_release) VALUES
    ('42510037', '2023-10-01', 7600.000, 95.00, 700.000, 400.200),
    ('42510037', '2023-11-01', 7650.000, 96.00, 710.000, 410.200),
    ('42510037', '2023-12-01', 7729.000, 99.90, 700.000, 400.200);


INSERT INTO specific_dam_analysis (
    dam_id,
    analysis_date,
    avg_storage_volume_12_months,
    avg_storage_volume_5_years,
    avg_storage_volume_20_years,
    avg_percentage_full_12_months,
    avg_percentage_full_5_years,
    avg_percentage_full_20_years,
    avg_storage_inflow_12_months,
    avg_storage_inflow_5_years,
    avg_storage_inflow_20_years,
    avg_storage_release_12_months,
    avg_storage_release_5_years,
    avg_storage_release_20_years
) VALUES
    -- Toonumbar Dam Analysis on 2024-11-01
    ('203042', '2024-11-01', 10500.000, 10300.000, 10000.000, 97.00, 95.00, 93.00, 500.500, 480.500, 460.500, 300.300, 290.300, 280.300),

    -- Glenbawn Dam Analysis on 2024-11-01
    ('210097', '2024-11-01', 730000.000, 720000.000, 700000.000, 97.45, 95.00, 93.00, 2200.200, 2100.200, 2000.200, 1600.000, 1500.000, 1400.000),

    -- Lostock Dam Analysis on 2024-11-01
    ('210102', '2024-11-01', 19500.000, 19000.000, 18500.000, 98.77, 96.00, 94.00, 600.000, 580.000, 560.000, 350.800, 340.800, 330.800),

    -- Glennies Creek Dam Analysis on 2024-11-01
    ('210117', '2024-11-01', 282303.000, 275000.000, 260000.000, 99.50, 97.00, 95.00, 1800.500, 1750.500, 1700.500, 1300.300, 1250.300, 1200.300),

    -- Warragamba Dam Analysis on 2024-11-01
    ('212243', '2024-11-01', 2064680.000, 2050000.000, 2000000.000, 100.00, 98.00, 96.00, 2500.700, 2400.700, 2300.700, 1800.600, 1700.600, 1600.600),

    -- Blowering Dam Analysis on 2024-11-01
    ('410102', '2024-11-01', 1603000.000, 1580000.000, 1550000.000, 99.90, 98.00, 96.00, 2000.500, 1950.500, 1900.500, 1500.300, 1450.300, 1400.300),

    -- Burrinjuck Dam Analysis on 2024-11-01
    ('410131', '2024-11-01', 1024750.000, 1010000.000, 990000.000, 99.00, 98.00, 97.00, 2070.800, 2050.800, 2030.800, 1540.300, 1520.300, 1500.300),

    -- Lake Wyangala Analysis on 2024-11-01
    ('412010', '2024-11-01', 1217035.000, 1200000.000, 1180000.000, 99.00, 98.00, 96.00, 2120.600, 2100.600, 2080.600, 1570.500, 1550.500, 1530.500),

    -- Lake Cargelligo Analysis on 2024-11-01
    ('412107', '2024-11-01', 30000.000, 29500.000, 29000.000, 99.80, 98.50, 97.00, 620.100, 610.100, 600.100, 360.900, 350.900, 340.900);

INSERT INTO overall_dam_analysis (
    analysis_date,
    avg_storage_volume_12_months,
    avg_storage_volume_5_years,
    avg_storage_volume_20_years,
    avg_percentage_full_12_months,
    avg_percentage_full_5_years,
    avg_percentage_full_20_years,
    avg_storage_inflow_12_months,
    avg_storage_inflow_5_years,
    avg_storage_inflow_20_years,
    avg_storage_release_12_months,
    avg_storage_release_5_years,
    avg_storage_release_20_years
) VALUES
    ('2024-11-25', 
        500000.000, 480000.000, 450000.000,
        98.50, 96.00, 94.00,
        1500.000, 1400.000, 1300.000,
        1100.000, 1000.000, 900.000
    );
