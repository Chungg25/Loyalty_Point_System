create database Advertising_Service;
use Advertising_Service;
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