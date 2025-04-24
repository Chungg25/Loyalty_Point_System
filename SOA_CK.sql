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
  brand_name VARCHAR(50) NOT NULL,
  title VARCHAR(100) NOT NULL,
  description VARCHAR(200) NOT NULL,
  points_required INT NOT NULL,
  reward VARCHAR(50) NOT NULL,
  start_at datetime NOT NULL,
  end_at datetime NOT NULL,
  status VARCHAR(50) NOT NULL,
  created_at datetime NOT NULL,
  PRIMARY KEY (campaign_id)
);

CREATE TABLE Campaign_Redemption
(
  campaign_redemption_id INT NOT NULL,
  campaign_id INT NOT NULL,
  points_spent INT NOT NULL,
  redeemed_at datetime NOT NULL,
  redemption_code VARCHAR(50) NOT NULL,
  PRIMARY KEY (campaign_redemption_id),
  FOREIGN KEY (campaign_id) REFERENCES Campaign(campaign_id)
);

create database Notification_Service
go
use Notification_Service

CREATE TABLE Notification
(
  notification_id INT AUTO_INCREMENT NOT NULL,
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
  user_id INT NOT NULL,         -- cho dễ truy vấn theo user
  type VARCHAR(20) NOT NULL CHECK (type IN ('EARN', 'REDEEM')),
  source_type VARCHAR(20) NOT NULL CHECK (source_type IN ('TRANSACTION', 'CAMPAIGN')),
  source_id INT NOT NULL,
  points INT NOT NULL,
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
  user_snapshot NVARCHAR(MAX),
  PRIMARY KEY (transaction_id)
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

-- Insert người dùng vào bảng Users với vai trò Customer
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

