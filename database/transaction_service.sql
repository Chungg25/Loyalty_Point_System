create database Transaction_Service;
use Transaction_Service;

CREATE TABLE User_Snapshot
(
  user_snapshot_id int not null AUTO_INCREMENT PRIMARY KEY,
	fullname varchar(20) not null,
	email varchar(20) not null,
	phone varchar(20) not null
);
CREATE TABLE Transactions (
  transaction_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  brand_id INT NOT NULL,
  invoice_code VARCHAR(50) NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  created_at DATETIME NOT NULL,
  user_snapshot_id INT,
  FOREIGN KEY (user_snapshot_id) REFERENCES user_snapshot(user_snapshot_id)
);

INSERT INTO User_Snapshot (fullname, email, phone)
SELECT 
  up.fullname,
  up.email,
  up.phone
FROM user_service.user_profile up
WHERE up.user_id = 1;
INSERT INTO User_Snapshot (fullname, email, phone)
SELECT 
  up.fullname,
  up.email,
  up.phone
FROM user_service.user_profile up
WHERE up.user_id = 2;
INSERT INTO User_Snapshot (fullname, email, phone)
SELECT 
  up.fullname,
  up.email,
  up.phone
FROM user_service.user_profile up
WHERE up.user_id = 3;
INSERT INTO User_Snapshot (fullname, email, phone)
SELECT 
  up.fullname,
  up.email,
  up.phone
FROM user_service.user_profile up
WHERE up.user_id = 4;
INSERT INTO User_Snapshot (fullname, email, phone)
SELECT 
  up.fullname,
  up.email,
  up.phone
FROM user_service.user_profile up
WHERE up.user_id = 5;
INSERT INTO User_Snapshot (fullname, email, phone)
SELECT 
  up.fullname,
  up.email,
  up.phone
FROM user_service.user_profile up
WHERE up.user_id = 6;
INSERT INTO User_Snapshot (fullname, email, phone)
SELECT 
  up.fullname,
  up.email,
  up.phone
FROM user_service.user_profile up
WHERE up.user_id = 7;
INSERT INTO User_Snapshot (fullname, email, phone)
SELECT 
  up.fullname,
  up.email,
  up.phone
FROM user_service.user_profile up
WHERE up.user_id = 8;
INSERT INTO User_Snapshot (fullname, email, phone)
SELECT 
  up.fullname,
  up.email,
  up.phone
FROM user_service.user_profile up
WHERE up.user_id = 9;
INSERT INTO User_Snapshot (fullname, email, phone)
SELECT 
  up.fullname,
  up.email,
  up.phone
FROM user_service.user_profile up
WHERE up.user_id = 10;

INSERT INTO Transactions (transaction_id, user_id, brand_id, invoice_code, amount, created_at, user_snapshot_id) VALUES
(1, 1, 1, 'INV-001', 100000, NOW(), 1),
(2, 2, 1, 'INV-002', 200000, NOW(), 2),
(3, 3, 2, 'INV-003', 150000, NOW(), 3),
(4, 4, 2, 'INV-004', 300000, NOW(), 4),
(5, 5, 3, 'INV-005', 180000, NOW(), 5),
(6, 1, 3, 'INV-006', 210000, NOW(), 1),
(7, 2, 4, 'INV-007', 250000, NOW(), 2),
(8, 3, 4, 'INV-008', 275000, NOW(), 3),
(9, 4, 5, 'INV-009', 120000, NOW(), 4),
(10, 5, 5, 'INV-010', 230000, NOW(), 5),

(11, 1, 1, 'INV-011', 198000, NOW(), 1),
(12, 2, 1, 'INV-012', 270000, NOW(), 2),
(13, 3, 2, 'INV-013', 145000, NOW(), 3),
(14, 4, 2, 'INV-014', 350000, NOW(), 4),
(15, 5, 3, 'INV-015', 160000, NOW(), 5),
(16, 1, 3, 'INV-016', 275000, NOW(), 1),
(17, 2, 4, 'INV-017', 310000, NOW(), 2),
(18, 3, 4, 'INV-018', 135000, NOW(), 3),
(19, 4, 5, 'INV-019', 200000, NOW(), 4),
(20, 5, 5, 'INV-020', 215000, NOW(), 5),

(21, 1, 1, 'INV-021', 190000, NOW(), 1),
(22, 2, 1, 'INV-022', 165000, NOW(), 2),
(23, 3, 2, 'INV-023', 275000, NOW(), 3),
(24, 4, 2, 'INV-024', 295000, NOW(), 4),
(25, 5, 3, 'INV-025', 188000, NOW(), 5),
(26, 1, 3, 'INV-026', 205000, NOW(), 1),
(27, 2, 4, 'INV-027', 225000, NOW(), 2),
(28, 3, 4, 'INV-028', 170000, NOW(), 3),
(29, 4, 5, 'INV-029', 265000, NOW(), 4),
(30, 5, 5, 'INV-030', 180000, NOW(), 5),

(31, 1, 1, 'INV-031', 240000, NOW(), 1),
(32, 2, 1, 'INV-032', 205000, NOW(), 2),
(33, 3, 2, 'INV-033', 300000, NOW(), 3),
(34, 4, 2, 'INV-034', 330000, NOW(), 4),
(35, 5, 3, 'INV-035', 100000, NOW(), 5),
(36, 1, 3, 'INV-036', 235000, NOW(), 1),
(37, 2, 4, 'INV-037', 210000, NOW(), 2),
(38, 3, 4, 'INV-038', 180000, NOW(), 3),
(39, 4, 5, 'INV-039', 195000, NOW(), 4),
(40, 5, 5, 'INV-040', 250000, NOW(), 5),

(41, 1, 1, 'INV-041', 175000, NOW(), 1),
(42, 2, 1, 'INV-042', 290000, NOW(), 2),
(43, 3, 2, 'INV-043', 270000, NOW(), 3),
(44, 4, 2, 'INV-044', 185000, NOW(), 4),
(45, 5, 3, 'INV-045', 245000, NOW(), 5),
(46, 1, 3, 'INV-046', 220000, NOW(), 1),
(47, 2, 4, 'INV-047', 260000, NOW(), 2),
(48, 3, 4, 'INV-048', 195000, NOW(), 3),
(49, 4, 5, 'INV-049', 235000, NOW(), 4),
(50, 5, 5, 'INV-050', 200000, NOW(), 5);









