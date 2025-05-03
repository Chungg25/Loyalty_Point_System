import qrcode
import json
from urllib.parse import urlencode

# Thông tin giao dịch mẫu
transaction_data = {
    "user_id": 1,
    "brand_id": 1,
    "invoice_code": "INV0010",
    "amount": 2750000,
    "created_at": "2025-04-27 10:30:00",
    "user_snapshot_id": 1,
}

# Đường dẫn API gốc
html_page_url = "http://192.168.1.13:5000/user/transaction_qr"

# Encode dữ liệu vào URL
query_string = urlencode(transaction_data)
full_url = f"{html_page_url}?{query_string}"

# Tạo QR Code
qr = qrcode.make(full_url)

# Lưu QR Code thành file
qr.save("transaction_qr.png")

print("Đã tạo mã QR chứa thông tin giao dịch!")