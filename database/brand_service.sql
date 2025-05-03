create database Brand_Service;
use Brand_Service;

CREATE TABLE Brand
(
  brand_id INT NOT NULL,
  brandname VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  status bit NOT NULL,
  coefficient FLOAT NOT NULL CHECK (coefficient >= 0),
  PRIMARY KEY (brand_id)
);

CREATE TABLE Contract
(
  contract_id INT NOT NULL,
  brand_id INT NOT NULL,
  user_id INT NOT NULL,
  start_at datetime NOT NULL,
  end_at datetime NOT NULL,
  status bit NOT NULL,
  created_at datetime NOT NULL,
  PRIMARY KEY (contract_id),
  FOREIGN KEY (brand_id) REFERENCES Brand(brand_id)
);

CREATE TABLE Category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

INSERT INTO Brand (brand_id, brandname, email, status, coefficient)
VALUES
(1, 'BrandA', 'contact@branda.com', '1', 1.5),
(2, 'BrandB', 'contact@brandb.com', '1', 1.8),
(3, 'BrandC', 'contact@brandc.com', '1', 1.2),
(4, 'BrandD', 'contact@brandd.com', '1', 2.0),
(5, 'BrandE', 'contact@brande.com', '1', 1.7);

INSERT INTO Contract (contract_id, brand_id, user_id, start_at, end_at, status, created_at)
VALUES
(1, 1, 6, '2025-04-21', '2026-04-21', 1, '2025-04-20 09:00:00'),
(2, 2, 6, '2025-04-21', '2026-04-21', 1, '2024-04-10 10:00:00'),
(3, 3, 7, '2025-04-21', '2027-04-21', 1, '2025-04-15 11:00:00'),
(4, 4, 6, '2025-04-21', '2026-04-21', 1, '2025-04-18 12:00:00'),
(5, 5, 7, '2025-04-21', '2028-04-21', 1, '2025-04-20 13:00:00'),
(6, 1, 6, '2022-04-20', '2023-04-20', 0, '2022-04-10 23:00:00'),
(7, 2, 7, '2023-12-20', '2024-12-20', 0, '2023-12-01 23:00:00'),
(8, 3, 6, '2020-04-21', '2021-04-21', 0, '2020-04-20 11:00:00'),
(9, 4, 6, '2021-04-21', '2022-04-21', 0, '2021-03-31 12:00:00');

INSERT INTO Category (name) VALUES
('Thời trang'),
('F&B'),
('Điện tử'),
('Mỹ Phẩm');