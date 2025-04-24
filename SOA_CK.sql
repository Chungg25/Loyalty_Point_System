-- Tạo database
CREATE DATABASE IF NOT EXISTS user_service;
USE user_service;

-- Bảng Users
CREATE TABLE Users (
  user_id INT NOT NULL PRIMARY KEY,
  username VARCHAR(30) NOT NULL,
  password VARCHAR(20) NOT NULL,
  created_at DATETIME NOT NULL,
  status BOOLEAN NOT NULL
);

-- Bảng User_Profile
CREATE TABLE User_Profile (
  user_profile_id INT NOT NULL PRIMARY KEY,
  fullname VARCHAR(50) NOT NULL,
  date_of_birth DATE NOT NULL,
  address VARCHAR(100) NOT NULL,
  email VARCHAR(50) NOT NULL,
  gender BOOLEAN NOT NULL,
  phone VARCHAR(10) NOT NULL,
  user_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Bảng Customer
CREATE TABLE Customer (
  membertype INT NOT NULL,
  user_id INT NOT NULL PRIMARY KEY,
  FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Bảng Mall
CREATE TABLE Mall (
  mall_id INT NOT NULL,
  user_id INT NOT NULL PRIMARY KEY,
  FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Bảng Brand
CREATE TABLE Brand (
  brand_id INT NOT NULL,
  user_id INT NOT NULL PRIMARY KEY,
  FOREIGN KEY (user_id) REFERENCES Users(user_id)
);


create database Brand_Service
go
use Brand_Service

CREATE TABLE Brand
(
  brand_id INT NOT NULL,
  brandname VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  status VARCHAR(20) NOT NULL,
  coefficient FLOAT NOT NULL CHECK (coefficient >= 0),
  created_at datetime NOT NULL,
  end_at datetime NOT NULL,
  PRIMARY KEY (brand_id)
);

create database Campaign_Service
go
use Campaign_Service

CREATE TABLE Campaign
(
  campaign_id INT NOT NULL,
  brand_id VARCHAR(50) NOT NULL,
  title VARCHAR(100) NOT NULL,
  description VARCHAR(200) NOT NULL,
  points_required INT NOT NULL,
  reward VARCHAR(50) NOT NULL,
  created_at datetime NOT NULL,
  start_at datetime NOT NULL,
  end_at datetime NOT NULL,
  status VARCHAR(50) NOT NULL,
  PRIMARY KEY (campaign_id)
);

CREATE TABLE Campaign_Redemption
(
  campaign_redemption_id INT NOT NULL,
  campaign_id INT NOT NULL,
  points_spent INT NOT NULL,
  redeemed_at datetime NOT NULL,
  PRIMARY KEY (campaign_redemption_id),
  FOREIGN KEY (campaign_id) REFERENCES Campaign(campaign_id)
);

CREATE TABLE discount_codes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(10) NOT NULL UNIQUE,
  campaign_id INT NOT NULL,
  user_id INT NOT NULL,
  created_at DATETIME NOT NULL,
  is_used BOOLEAN DEFAULT FALSE,
  expired_at DATETIME,
  FOREIGN KEY (campaign_id) REFERENCES Campaign(campaign_id)
);


create database Notification_Service
go
use Notification_Service

CREATE TABLE Notification
(
<<<<<<< HEAD
  notification_id INT AUTO_INCREMENT NOT NULL,
=======
  notification_id INT NOT NULL,
  user_id INT NOT NULL,
>>>>>>> 7dee5e481f144bf5a1191117fa3f6ee683e28096
  title VARCHAR(100) NOT NULL,
  message VARCHAR(100) NOT NULL,
  created_at datetime NOT NULL,
  end_at datetime,
  status bit NOT NULL,
  PRIMARY KEY (notification_id)
);

create database Point_Service
go
use Point_Service
-- Ví: Ví điểm của từng user
CREATE TABLE PointWallet (
  point_wallet_id INT IDENTITY(1,1) PRIMARY KEY,
  user_id INT NOT NULL, -- từ User_Service
  total_points INT NOT NULL DEFAULT 0, -- tổng điểm hiện tại
  last_update DATETIME NOT NULL DEFAULT GETDATE()
);

-- Nhật ký điểm: dùng để log cả tích điểm (earn) lẫn sử dụng điểm (redeem)
CREATE TABLE Point_Log (
  point_log_id INT IDENTITY(1,1) PRIMARY KEY,
  point_wallet_id INT NOT NULL,
  type VARCHAR(20) NOT NULL CHECK (type IN ('EARN', 'REDEEM')),
  source_type VARCHAR(20) NOT NULL CHECK (source_type IN ('TRANSACTION', 'CAMPAIGN')),
  source_id INT NOT NULL,
  points INT NOT NULL,
  metadata NVARCHAR(MAX),
  description VARCHAR(200) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT GETDATE(),
  FOREIGN KEY (point_wallet_id) REFERENCES PointWallet(point_wallet_id)
);

create database Transaction_Service
go
use Transaction_Service

CREATE TABLE User_Snapshot
(
	user_snapshot_id int not null AUTO_INCREMENT,
	fullname varchar(20) not null,
	email varchar(20) not null,
	phone varchar(20) not null
);
CREATE TABLE Transactions (
  transaction_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  brand_id INT NOT NULL,
  invoice_code VARCHAR(50) NOT NULL,
<<<<<<< HEAD
  amount decimal(10, 2) NOT NULL,
  created_at datetime NOT NULL,
  user_snapshot NVARCHAR(MAX),
  PRIMARY KEY (transaction_id)
=======
  amount DECIMAL(10,2) NOT NULL,
  created_at DATETIME NOT NULL,
  user_snapshot_id INT,
  FOREIGN KEY (user_snapshot_id) REFERENCES user_snapshot(user_snapshot_id)
>>>>>>> 7dee5e481f144bf5a1191117fa3f6ee683e28096
);

create database Advertising_Service
go
use Advertising_Service
CREATE TABLE Ad
(
  ad_id INT NOT NULL,
  brand_id INT NOT NULL,
  title VARCHAR(100) NOT NULL,
  description VARCHAR(200) NOT NULL,
  start_at datetime NOT NULL,
  end_at datetime NOT NULL,
  created_at datetime NOT NULL,
  PRIMARY KEY (ad_id)
);
-- Insert dữ liệu mẫu cho bảng Users
INSERT INTO Users (user_id, username, password, created_at, status) VALUES
(1, 'john_doe', 'pass123', '2025-04-23 18:06:13', 1),
(2, 'alice_smith', 'pass456', '2025-04-23 18:06:13', 1),
(3, 'bob_nguyen', 'pass789', '2025-04-23 18:06:13', 1),
(4, 'carol_tran', 'passabc', '2025-04-23 18:06:13', 1),
(5, 'david_phan', 'passdef', '2025-04-23 18:06:13', 1),
(6, 'mall_admin1', 'mall123', '2025-04-23 18:06:13', 1),
(7, 'mall_admin2', 'mall456', '2025-04-23 18:06:13', 1),
(8, 'brand_lv', 'brand123', '2025-04-23 18:06:13', 1),
(9, 'brand_chanel', 'brand456', '2025-04-23 18:06:13', 1),
(10, 'brand_dior', 'brand789', '2025-04-23 18:06:13', 1),
(11, 'brand_prada', '123', '2025-04-23 18:25:18', 1),
(12, 'brand_celine', '123', '2025-04-23 18:25:18', 1);
-- Insert dữ liệu mẫu cho bảng User_Profile
INSERT INTO User_Profile (user_profile_id, fullname, date_of_birth, address, email, gender, phone, user_id) VALUES
(1, 'John Doe', '1990-01-01', '123 Lê Lợi, Q1', 'john@example.com', 1, '0901111111', 1),
(2, 'Alice Smith', '1985-02-02', '456 Hai Bà Trưng, Q3', 'alice@example.com', 0, '0902222222', 2),
(3, 'Bob Nguyễn', '1992-03-03', '789 Pasteur, Q5', 'bob@example.com', 1, '0903333333', 3),
(4, 'Carol Trần', '1994-04-04', '101 Trần Hưng Đạo, Q1', 'carol@example.com', 0, '0904444444', 4),
(5, 'David Phan', '1996-05-05', '202 Nguyễn Huệ, Q1', 'david@example.com', 1, '0905555555', 5),
(6, 'Mall Admin 1', '1980-06-06', '88 Mall St', 'mall1@mall.com', 1, '0906666666', 6),
(7, 'Mall Admin 2', '1981-07-07', '89 Mall St', 'mall2@mail.com', 0, '0907777777', 7),
(8, 'Brand Owner 1', '1982-08-08', '100 Brand Blvd', 'brand1@brand.com', 1, '0908888888', 8),
(9, 'Brand Owner 2', '1983-09-09', '101 Brand Blvd', 'brand2@brand.com', 0, '0909999999', 9),
(10, 'Brand Owner 3', '1984-10-10', '102 Brand Blvd', 'brand3@brand.com', 1, '0910000000', 10),
(11, 'Brand Owner 4', '1993-10-09', '102 Brand Blvd', 'brand4@brand.com', 0, '0909999999', 11),
(12, 'Brand Owner 5', '1999-10-10', '102 Brand Blvd', 'brand5@brand.com', 1, '0910000000', 12);
-- Insert dữ liệu mẫu cho bảng Customer, Mall, Brand
INSERT INTO Customer (membertype, user_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(1, 4),
(2, 5);
INSERT INTO Mall (mall_id, user_id) VALUES
(1, 6),
(2, 7);
INSERT INTO Brand (brand_id, user_id) VALUES
(1, 8),
(2, 9),
(3, 10),
(4, 11),
(5, 12);

-- Insert thông tin chi tiết cho bảng user_snapshot
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

-- Insert thông tin chi tiết cho bảng Transactions
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

--Cập nhật membertype
UPDATE Customer SET membertype = 1 WHERE user_id IN (1, 2);
UPDATE Customer SET membertype = 2 WHERE user_id IN (3);
UPDATE Customer SET membertype = 3 WHERE user_id IN (4,5);


INSERT INTO PointWallet (user_id, total_points, last_update)
SELECT u.user_id,
       CASE c.membertype
           WHEN 1 THEN 50
           WHEN 2 THEN 100
           WHEN 3 THEN 150
           ELSE 0
       END AS total_points,
       CURRENT_TIMESTAMP
FROM User_Service.Users u
JOIN User_Service.Customer c ON u.user_id = c.user_id;

-- Cập nhật điểm 
UPDATE PointWallet pw
JOIN (
  SELECT 
    t.user_id,
    SUM(FLOOR(t.amount / 10000 * b.coefficient)) AS earned_points
  FROM Transaction_Service.Transactions t
  JOIN Brand_Service.Brand b ON t.brand_id = b.brand_id
  LEFT JOIN Point_Log pl 
    ON pl.source_id = t.transaction_id 
    AND pl.source_type = 'TRANSACTION' 
    AND pl.type = 'EARN'
  WHERE pl.point_log_id IS NULL  -- chỉ lấy giao dịch chưa log
  GROUP BY t.user_id
) AS points_per_user ON pw.user_id = points_per_user.user_id
SET 
  pw.total_points = pw.total_points + points_per_user.earned_points,
  pw.last_update = CURRENT_TIMESTAMP;

-- Ghi nhận điểm

INSERT INTO Point_Log (
  point_wallet_id, type, source_type, source_id, points, metadata, description, created_at
)
SELECT 
  pw.point_wallet_id,
  'EARN',
  'TRANSACTION',
  t.transaction_id,
  FLOOR(t.amount / 10000 * b.coefficient),
  NULL,
  CONCAT('Tích điểm từ hóa đơn ', t.invoice_code),
  CURRENT_TIMESTAMP
FROM Transaction_Service.Transactions t
JOIN Brand_Service.Brand b ON t.brand_id = b.brand_id
JOIN PointWallet pw ON pw.user_id = t.user_id
LEFT JOIN Point_Log pl 
  ON pl.source_id = t.transaction_id AND pl.source_type = 'TRANSACTION' AND pl.type = 'EARN'
WHERE pl.point_log_id IS NULL;

create database Voucher_Service
go
use Voucher_Service
CREATE TABLE Voucher 
(
  voucher_id INT AUTO_INCREMENT PRIMARY KEY,
  brand_id INT DEFAULT NULL,
  title VARCHAR(255),
  description TEXT,
  points_required INT,
  discount_amount DECIMAL(10,2),
  created_at DATETIME,
  start_at DATETIME,
  end_at DATETIME,
  approval_comment TEXT
);

CREATE TABLE Voucher_Redemption (
  redemption_id INT AUTO_INCREMENT PRIMARY KEY,
  voucher_id INT,
  user_id INT,
  points_spent INT,
  redeemed_at DATETIME,
  redemption_code VARCHAR(100),
  user_snapshot NVARCHAR(MAX)
);

