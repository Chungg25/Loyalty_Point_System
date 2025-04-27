create database Notification_Service;
use Notification_Service;

CREATE TABLE Notification
(
  notification_id INT AUTO_INCREMENT,
  title VARCHAR(100) NOT NULL,
  message VARCHAR(100) NOT NULL,
  created_at datetime NOT NULL,
  end_at datetime,
  status bit NOT NULL,
  PRIMARY KEY (notification_id)
);

INSERT INTO Notification (notification_id, title, message, created_at, end_at, status) VALUES
(1, 'Khuyến mãi đặc biệt', 'Nhận ngay 20% điểm thưởng cho đơn hàng đầu tiên!', '2025-04-21 10:00:00', '2025-05-21 10:00:00', 1),
(2, 'Giảm giá mùa hè', 'Giảm giá 30% cho tất cả sản phẩm trong tháng 6!', '2025-04-22 11:00:00', '2025-06-30 11:00:00', 1),
(3, 'Chương trình tích điểm', 'Tích lũy điểm thưởng cho mỗi giao dịch!', '2025-04-23 12:00:00', NULL, 1),
(4, 'Khuyến mãi sinh nhật', 'Nhận ngay 50% điểm thưởng trong tháng sinh nhật của bạn!', '2025-04-24 13:00:00', NULL, 1),
(5, 'Giảm giá đặc biệt', 'Giảm giá 15% cho đơn hàng trên 1 triệu đồng!', '2025-04-25 14:00:00', '2025-05-25 14:00:00', 1),
(6, 'Chương trình giới thiệu bạn bè', 'Giới thiệu bạn bè và nhận ngay 100.000 VNĐ vào ví!', '2025-04-26 15:00:00', NULL, 1),
(7, 'Khuyến mãi cuối tuần', 'Giảm giá 20% cho tất cả sản phẩm vào cuối tuần này!', '2025-04-27 16:00:00', NULL, 1),
(8, 'Chương trình khách hàng thân thiết', 'Nhận ngay ưu đãi đặc biệt cho khách hàng thân thiết!', '2025-04-28 17:00:00', NULL, 1),
(9, 'Khuyến mãi mùa đông', 'Giảm giá 25% cho tất cả sản phẩm trong tháng 12!', '2025-04-29 18:00:00', NULL, 1),
(10, 'Chương trình hoàn tiền', 'Hoàn tiền 10% cho mỗi giao dịch thành công!', '2025-04-30 19:00:00', NULL, 1);
