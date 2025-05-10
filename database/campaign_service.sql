create database Campaign_Service;
use Campaign_Service;

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
  redemption_code VARCHAR(6) NULl
  PRIMARY KEY (campaign_id)
);

CREATE TABLE Campaign_Redemption
(
  campaign_redemption_id INT NOT NULL,
  campaign_id INT NOT NULL,
  user_id INT NOT NULL,
  points_spent INT NOT NULL,
  redeemed_at datetime NOT NULL,
  PRIMARY KEY (campaign_redemption_id),
  FOREIGN KEY (campaign_id) REFERENCES Campaign(campaign_id)
);

INSERT INTO Campaign (brand_id, title, description, points_required, reward, created_at, start_at, end_at, status, redemption_code)
VALUES
('1', 'Chiến dịch Mùa Hè', 'Ưu đãi giảm giá mùa hè', 500, 'Discount 20%', NOW(), NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY), 'Đang hoạt động', 'A1B2C3'),
('1', 'Chiến dịch Noel', 'Quà tặng Giáng sinh cho khách hàng', 700, 'Voucher 100K', NOW(), NOW(), DATE_ADD(NOW(), INTERVAL 60 DAY), 'Đang hoạt động', 'D4E5F6'),
('1', 'Back to School', 'Ưu đãi mùa tựu trường', 400, 'Discount 15%', NOW(), NOW(), DATE_ADD(NOW(), INTERVAL 45 DAY), 'Sắp bắt đầu', 'G7H8I9'),
('1', 'Mừng Sinh Nhật', 'Voucher mừng sinh nhật khách hàng', 800, 'Voucher 200K', NOW(), NOW(), DATE_ADD(NOW(), INTERVAL 20 DAY), 'Đang hoạt động', 'J1K2L3'),
('1', 'Tích điểm đổi quà', 'Tích điểm đổi quà hấp dẫn', 300, 'Tích điểm', NOW(), NOW(), DATE_ADD(NOW(), INTERVAL 90 DAY), 'Đang hoạt động', 'M4N5O6'),
('1', 'Flash Sale 11.11', 'Giảm giá trong ngày siêu sale', 200, 'Discount 30%', NOW(), NOW(), DATE_ADD(NOW(), INTERVAL 1 DAY), 'Kết thúc', 'P7Q8R9'),
('1', 'Khách VIP ưu đãi', 'Ưu đãi đặc biệt cho khách VIP', 1000, 'Voucher 500K', NOW(), NOW(), DATE_ADD(NOW(), INTERVAL 15 DAY), 'Đang hoạt động', 'S1T2U3'),
('1', 'Cuối năm rộn ràng', 'Quà tặng cuối năm ấm áp', 600, 'Discount 10%', NOW(), NOW(), DATE_ADD(NOW(), INTERVAL 40 DAY), 'Đang hoạt động', 'V4W5X6'),
('1', 'Black Friday', 'Siêu ưu đãi Black Friday', 500, 'Discount 50%', NOW(), NOW(), DATE_ADD(NOW(), INTERVAL 2 DAY), 'Kết thúc', 'Y7Z8A9'),
('1', 'Tết Nguyên Đán', 'Ưu đãi mừng Tết', 900, 'Voucher 300K', NOW(), NOW(), DATE_ADD(NOW(), INTERVAL 70 DAY), 'Sắp bắt đầu', 'B1C2D3');

ALTER TABLE Campaign_Redemption
ADD COLUMN status ENUM('Chưa sử dụng', 'Đã sử dụng', 'Hết hạn') DEFAULT 'Chưa sử dụng';