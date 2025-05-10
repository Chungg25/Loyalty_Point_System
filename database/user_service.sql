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
-- CREATE TABLE Customer (
--   membertype INT NOT NULL,
--   user_id INT NOT NULL PRIMARY KEY,
--   FOREIGN KEY (membertype) REFERENCES Users(membertype)
-- );

-- Bảng Customer (sửa FOREIGN KEY đúng tới MemberTypeCoefficient)
CREATE TABLE Customer (
  membertype INT NOT NULL,
  user_id INT NOT NULL PRIMARY KEY,
  FOREIGN KEY (user_id) REFERENCES Users(user_id)
);


CREATE TABLE MemberTypeCoefficient (
  membertype INT PRIMARY KEY,
  member_coefficient FLOAT NOT NULL
);

-- Thêm hệ số cho từng hạng
INSERT INTO MemberTypeCoefficient (membertype, member_coefficient) VALUES
  (1, 1.0),   -- Thành viên Bạc
  (2, 1.2),   -- Thành viên Vàng
  (3, 1.5);   -- Thành viên Kim cương


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

UPDATE Customer SET membertype = 1 WHERE user_id IN (1, 2);
UPDATE Customer SET membertype = 2 WHERE user_id IN (3);
UPDATE Customer SET membertype = 3 WHERE user_id IN (4,5);