create database User_Service
go
use User_Service

CREATE TABLE Users
(
  user_id INT NOT NULL,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(50) NOT NULL,
  role VARCHAR(50) NOT NULL,
  created_at datetime NOT NULL,
  status bit NOT NULL,
  PRIMARY KEY (user_id)
);

CREATE TABLE User_Profile
(
  user_profile_id INT NOT NULL,
  user_id INT NOT NULL,
  fullname VARCHAR(50) NOT NULL,
  date_of_birth datetime NOT NULL,
  address VARCHAR(100) NOT NULL,
  gender bit NOT NULL,
  membertype INT NOT NULL,
  phone VARCHAR(10) NOT NULL,
  email VARCHAR(30) NOT NULL,
  PRIMARY KEY (user_profile_id),
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
  notification_id INT NOT NULL,
  user_id INT NOT NULL,
  title VARCHAR(100) NOT NULL,
  message VARCHAR(100) NOT NULL,
  created_at datetime NOT NULL,
  end_at datetime,
  PRIMARY KEY (notification_id)
);

create database Point_Service
go
use Point_Service

CREATE DATABASE Point_Service;
GO

USE Point_Service;

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

CREATE TABLE Transactions
(
  transaction_id INT NOT NULL,
  user_id INT NOT NULL,
  brand_id INT NOT NULL,
  invoice_code VARCHAR(50) NOT NULL,
  amount decimal(10, 2) NOT NULL,
  created_at datetime NOT NULL,
  user_snapshot_id NVARCHAR(MAX),
  PRIMARY KEY (transaction_id)
);

CREATE TABLE User_Snapshot
(
	user_snapshot_id int not null,
	fullname varchar(20) not null,
	email varchar(20) not null,
	phone varchar(20) not null
)

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
INSERT INTO Users (user_id, username, password, role, created_at, status)
VALUES
(1, 'john_doe', 'password123', 'Customer', '2025-04-21 10:00:00', 1),
(2, 'alice_smith', 'alicepassword', 'Customer', '2025-04-21 10:30:00', 1),
(3, 'bob_johnson', 'bobpassword', 'Customer', '2025-04-21 11:00:00', 1),
(4, 'carol_white', 'carolpassword', 'Customer', '2025-04-21 11:30:00', 1),
(5, 'david_brown', 'davidpassword', 'Customer', '2025-04-21 12:00:00', 1),
(6, 'eve_jones', 'evepassword', 'Customer', '2025-04-21 12:30:00', 1),
(7, 'frank_miller', 'frankpassword', 'Customer', '2025-04-21 13:00:00', 1),
(8, 'grace_davis', 'gracepassword', 'Customer', '2025-04-21 13:30:00', 1),
(9, 'hank_garcia', 'hankpassword', 'Customer', '2025-04-21 14:00:00', 1),
(10, 'iris_lee', 'irispw123', 'Customer', '2025-04-21 14:30:00', 1);


-- Insert thông tin chi tiết cho các khách hàng vào bảng User_Profile
INSERT INTO User_Profile (user_profile_id, user_id, fullname, date_of_birth, address, gender, membertype, phone, email)
VALUES
(1, 1, 'John Doe', '1990-01-15', '123 Đường ABC, Quận 1, TP.HCM', 1, 1, '0901234567', 'john.doe@example.com'),
(2, 2, 'Alice Smith', '1985-04-22', '456 Đường XYZ, Quận 3, TP.HCM', 0, 1, '0902345678', 'alice.smith@example.com'),
(3, 3, 'Bob Johnson', '1992-06-10', '789 Đường PQR, Quận 5, TP.HCM', 1, 1, '0903456789', 'bob.johnson@example.com'),
(4, 4, 'Carol White', '1988-08-25', '101 Đường DEF, Quận 7, TP.HCM', 0, 1, '0904567890', 'carol.white@example.com'),
(5, 5, 'David Brown', '1991-03-12', '202 Đường GHI, Quận 2, TP.HCM', 1, 1, '0905678901', 'david.brown@example.com'),
(6, 6, 'Eve Jones', '1993-09-17', '303 Đường JKL, Quận 8, TP.HCM', 0, 1, '0906789012', 'eve.jones@example.com'),
(7, 7, 'Frank Miller', '1989-12-01', '404 Đường MNO, Quận 9, TP.HCM', 1, 1, '0907890123', 'frank.miller@example.com'),
(8, 8, 'Grace Davis', '1994-07-05', '505 Đường STU, Quận 10, TP.HCM', 0, 1, '0908901234', 'grace.davis@example.com'),
(9, 9, 'Hank Garcia', '1990-11-20', '606 Đường VWX, Quận 11, TP.HCM', 1, 1, '0909012345', 'hank.garcia@example.com'),
(10, 10, 'Iris Lee', '1995-02-28', '707 Đường YZ, Quận 12, TP.HCM', 0, 1, '0900123456', 'iris.lee@example.com');

-- Insert thông tin chi tiết cho các thương hiệu  vào bảng Brand
INSERT INTO Brand (brand_id, brandname, email, status, coefficient, created_at, end_at)
VALUES
(1, 'LV', 'contact@branda.com', '1', 1.5, '2025-04-21 09:00:00', '2026-04-21 09:00:00'),
(2, 'Chanel', 'contact@brandb.com', '1', 1.8, '2025-04-21 10:00:00', '2026-04-21 10:00:00'),
(3, 'Dior', 'contact@brandc.com', '1', 1.2, '2025-04-21 11:00:00', '2026-04-21 11:00:00'),
(4, 'Prada', 'contact@brandd.com', '1', 2.0, '2025-04-21 12:00:00', '2026-04-21 12:00:00'),
(5, 'Celine', 'contact@brande.com', '1', 1.7, '2025-04-21 13:00:00', '2026-04-21 13:00:00');

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
INSERT INTO transactions (user_id, brand_id, invoice_code, amount, created_at, user_snapshot_id)
VALUES
(1, 1, 'INV-A-001', 253000, NOW(), 1),
(2, 2, 'INV-A-002', 467000, NOW(), 2),
(3, 3, 'INV-A-003', 121000, NOW(), 3),
(4, 4, 'INV-A-004', 891000, NOW(), 4),
(5, 5, 'INV-A-005', 378000, NOW(), 5),
(6, 1, 'INV-A-006', 645000, NOW(), 6),
(7, 2, 'INV-A-007', 210000, NOW(), 7),
(8, 3, 'INV-A-008', 999000, NOW(), 8),
(9, 4, 'INV-A-009', 488000, NOW(), 9),
(10, 5, 'INV-A-010', 302000, NOW(), 10),

(1, 1, 'INV-A-011', 180000, NOW(), 1),
(2, 2, 'INV-A-012', 765000, NOW(), 2),
(3, 3, 'INV-A-013', 905000, NOW(), 3),
(4, 4, 'INV-A-014', 470000, NOW(), 4),
(5, 5, 'INV-A-015', 150000, NOW(), 5),
(6, 1, 'INV-A-016', 620000, NOW(), 6),
(7, 2, 'INV-A-017', 730000, NOW(), 7),
(8, 3, 'INV-A-018', 440000, NOW(), 8),
(9, 4, 'INV-A-019', 810000, NOW(), 9),
(10, 5, 'INV-A-020', 299000, NOW(), 10),

(1, 2, 'INV-A-021', 388000, NOW(), 1),
(2, 3, 'INV-A-022', 560000, NOW(), 2),
(3, 4, 'INV-A-023', 215000, NOW(), 3),
(4, 5, 'INV-A-024', 623000, NOW(), 4),
(5, 1, 'INV-A-025', 347000, NOW(), 5),
(6, 2, 'INV-A-026', 980000, NOW(), 6),
(7, 3, 'INV-A-027', 429000, NOW(), 7),
(8, 4, 'INV-A-028', 395000, NOW(), 8),
(9, 5, 'INV-A-029', 155000, NOW(), 9),
(10, 1, 'INV-A-030', 810000, NOW(), 10),

(1, 3, 'INV-A-031', 460000, NOW(), 1),
(2, 4, 'INV-A-032', 920000, NOW(), 2),
(3, 5, 'INV-A-033', 490000, NOW(), 3),
(4, 1, 'INV-A-034', 325000, NOW(), 4),
(5, 2, 'INV-A-035', 278000, NOW(), 5),
(6, 3, 'INV-A-036', 300000, NOW(), 6),
(7, 4, 'INV-A-037', 187000, NOW(), 7),
(8, 5, 'INV-A-038', 330000, NOW(), 8),
(9, 1, 'INV-A-039', 576000, NOW(), 9),
(10, 2, 'INV-A-040', 654000, NOW(), 10),

(1, 4, 'INV-A-041', 110000, NOW(), 1),
(2, 5, 'INV-A-042', 870000, NOW(), 2),
(3, 1, 'INV-A-043', 980000, NOW(), 3),
(4, 2, 'INV-A-044', 245000, NOW(), 4),
(5, 3, 'INV-A-045', 365000, NOW(), 5),
(6, 4, 'INV-A-046', 405000, NOW(), 6),
(7, 5, 'INV-A-047', 999000, NOW(), 7),
(8, 1, 'INV-A-048', 530000, NOW(), 8),
(9, 2, 'INV-A-049', 612000, NOW(), 9),
(10, 3, 'INV-A-050', 777000, NOW(), 10);

--Cập nhật membertype
UPDATE User_Profile SET membertype = 1 WHERE user_id IN (1, 2, 3);
UPDATE User_Profile SET membertype = 2 WHERE user_id IN (4, 5, 6, 7);
UPDATE User_Profile SET membertype = 3 WHERE user_id IN (8, 9, 10);

-- Cập nhật điểm 
UPDATE PointWallet pw
JOIN (
  SELECT 
    t.user_id,
    SUM(FLOOR(t.amount / 1000 * b.coefficient)) AS earned_points
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
  FLOOR(t.amount / 1000 * b.coefficient),
  NULL,
  CONCAT('Tích điểm từ hóa đơn ', t.invoice_code),
  CURRENT_TIMESTAMP
FROM Transaction_Service.Transactions t
JOIN Brand_Service.Brand b ON t.brand_id = b.brand_id
JOIN PointWallet pw ON pw.user_id = t.user_id
LEFT JOIN Point_Log pl 
  ON pl.source_id = t.transaction_id AND pl.source_type = 'TRANSACTION' AND pl.type = 'EARN'
WHERE pl.point_log_id IS NULL;



