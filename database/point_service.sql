create database Point_Service;
use Point_Service;
CREATE TABLE PointWallet (
  point_wallet_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL, 
  total_points INT NOT NULL DEFAULT 0, 
  last_update DATETIME NOT NULL DEFAULT GETDATE()
);

CREATE TABLE Point_Log (
  point_log_id INT AUTO_INCREMENT PRIMARY KEY,
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

CREATE TABLE ConversionRule (
  rule_id INT AUTO_INCREMENT PRIMARY KEY,
  rate FLOAT NOT NULL,  
  effective_from DATETIME NOT NULL,
  effective_to DATETIME
);


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