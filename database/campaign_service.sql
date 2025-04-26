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
