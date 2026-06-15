-- ============================================================
-- PC Configurator — DML (Dati di test)
-- ============================================================

INSERT INTO "user" (username, email, password, role) VALUES
('admin', 'admin@pcconfig.it', 'admin123', 'admin');

-- CPU
INSERT INTO component (name, brand, category, price, wattage, stock, in_stock, description, specs) VALUES
('Ryzen 9 7950X',  'AMD',   'CPU', 699.99, 170, 15, TRUE, 'CPU AMD top di gamma', 'socket:AM5|cores:16|threads:32|tdp:170|boost_ghz:5.7'),
('Core i9-13900K', 'Intel', 'CPU', 589.99, 253, 12, TRUE, 'CPU Intel 13a gen',    'socket:LGA1700|cores:24|threads:32|tdp:253|boost_ghz:5.8'),
('Ryzen 5 7600X',  'AMD',   'CPU', 249.99, 105, 30, TRUE, 'CPU AMD mid-range',    'socket:AM5|cores:6|threads:12|tdp:105|boost_ghz:5.3');

-- Motherboard
INSERT INTO component (name, brand, category, price, wattage, stock, in_stock, description, specs) VALUES
('ROG Crosshair X670E', 'ASUS',   'Motherboard', 549.99, 0, 8,  TRUE, 'Scheda madre AM5 top',    'socket:AM5|form_factor:ATX|ddr:DDR5'),
('MAG Z790 Tomahawk',   'MSI',    'Motherboard', 299.99, 0, 20, TRUE, 'Scheda madre LGA1700',    'socket:LGA1700|form_factor:ATX|ddr:DDR5'),
('B650M Pro RS',        'ASRock', 'Motherboard', 149.99, 0, 25, TRUE, 'Scheda madre AM5 budget', 'socket:AM5|form_factor:mATX|ddr:DDR5');

-- RAM
INSERT INTO component (name, brand, category, price, wattage, stock, in_stock, description, specs) VALUES
('Trident Z5 RGB 32GB', 'G.Skill', 'RAM', 149.99, 5, 40, TRUE, 'Kit DDR5 6000MHz', 'type:DDR5|capacity_gb:32|speed_mhz:6000|cl:32'),
('Vengeance 16GB DDR5', 'Corsair', 'RAM',  79.99, 3, 50, TRUE, 'Kit DDR5 5200MHz', 'type:DDR5|capacity_gb:16|speed_mhz:5200|cl:38');

-- GPU
INSERT INTO component (name, brand, category, price, wattage, stock, in_stock, description, specs) VALUES
('GeForce RTX 4090',   'NVIDIA', 'GPU', 1599.99, 450, 5,  TRUE, 'GPU flagship NVIDIA', 'vram_gb:24|vram_type:GDDR6X|tdp:450'),
('Radeon RX 7900 XTX', 'AMD',    'GPU',  999.99, 355, 8,  TRUE, 'GPU top AMD RDNA3',   'vram_gb:24|vram_type:GDDR6|tdp:355'),
('GeForce RTX 4070',   'NVIDIA', 'GPU',  599.99, 200, 18, TRUE, 'GPU mid-range 1440p', 'vram_gb:12|vram_type:GDDR6X|tdp:200');

-- PSU
INSERT INTO component (name, brand, category, price, wattage, stock, in_stock, description, specs) VALUES
('RM1000x',      'Corsair',      'PSU', 189.99, 0, 15, TRUE, '1000W 80+ Gold',     'watt:1000|rating:80+Gold|modular:full'),
('Leadex V 850W','Super Flower', 'PSU', 139.99, 0, 20, TRUE, '850W 80+ Platinum',  'watt:850|rating:80+Platinum|modular:full'),
('Focus GX-650', 'Seasonic',     'PSU', 109.99, 0, 25, TRUE, '650W 80+ Gold',      'watt:650|rating:80+Gold|modular:full');

-- Storage
INSERT INTO component (name, brand, category, price, wattage, stock, in_stock, description, specs) VALUES
('980 Pro 2TB',    'Samsung', 'Storage', 179.99, 6, 30, TRUE, 'SSD NVMe PCIe 4.0', 'type:NVMe|capacity_gb:2000|interface:PCIe4.0'),
('SN850X 1TB',    'WD',      'Storage',  99.99, 5, 35, TRUE, 'SSD NVMe gaming',    'type:NVMe|capacity_gb:1000|interface:PCIe4.0'),
('Barracuda 4TB', 'Seagate', 'Storage',  79.99, 7, 20, TRUE, 'HDD 3.5" storage',   'type:HDD|capacity_gb:4000|rpm:7200');

-- Case
INSERT INTO component (name, brand, category, price, wattage, stock, in_stock, description, specs) VALUES
('Fractal Torrent',    'Fractal Design', 'Case', 169.99, 0, 12, TRUE, 'Case ATX airflow', 'form_factor:ATX|gpu_max_mm:461'),
('Lian Li PC-O11 Air', 'Lian Li',       'Case', 149.99, 0, 15, TRUE, 'Case ATX dual',    'form_factor:ATX|gpu_max_mm:420');

-- Cooler
INSERT INTO component (name, brand, category, price, wattage, stock, in_stock, description, specs) VALUES
('NH-D15',        'Noctua', 'Cooler',  99.99, 5, 20, TRUE, 'Dissipatore aria best-in-class', 'type:air|socket_am5:yes|socket_lga1700:yes|tdp_max:250'),
('Kraken X63',    'NZXT',   'Cooler', 129.99, 8, 18, TRUE, 'AIO 280mm RGB',                  'type:aio|radiator_mm:280|socket_am5:yes|socket_lga1700:yes'),
('Freezer II 360','Arctic', 'Cooler', 109.99, 7, 22, TRUE, 'AIO 360mm silenzioso',            'type:aio|radiator_mm:360|socket_am5:yes|socket_lga1700:yes');

-- Regole di compatibilità
-- CPU AM5 compatibili con Motherboard AM5
INSERT INTO compatibility_rule (component_a_id, component_b_id, is_compatible, reason) VALUES
(1, 4, TRUE,  'Entrambi socket AM5'),
(1, 6, TRUE,  'Entrambi socket AM5'),
(3, 4, TRUE,  'Entrambi socket AM5'),
(3, 6, TRUE,  'Entrambi socket AM5');

-- CPU AM5 incompatibili con Motherboard LGA1700
INSERT INTO compatibility_rule (component_a_id, component_b_id, is_compatible, reason) VALUES
(1, 5, FALSE, 'Socket incompatibile: CPU AM5, scheda madre LGA1700'),
(3, 5, FALSE, 'Socket incompatibile: CPU AM5, scheda madre LGA1700');

-- CPU LGA1700 compatibile con Motherboard LGA1700
INSERT INTO compatibility_rule (component_a_id, component_b_id, is_compatible, reason) VALUES
(2, 5, TRUE,  'Entrambi socket LGA1700');

-- CPU LGA1700 incompatibile con Motherboard AM5
INSERT INTO compatibility_rule (component_a_id, component_b_id, is_compatible, reason) VALUES
(2, 4, FALSE, 'Socket incompatibile: CPU LGA1700, scheda madre AM5'),
(2, 6, FALSE, 'Socket incompatibile: CPU LGA1700, scheda madre AM5');
