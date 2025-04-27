from flask import Flask, render_template, jsonify
from flask_cors import CORS
from user_service import user_bp
from brand_service import brand_bp
from campaign_service import campaign_bp
from notification_service import notification_bp
from transaction_service import transaction_bp
from point_service import point_bp
from voucher_service import voucher_bp

app = Flask(__name__)
CORS(app)

app.secret_key = 'abc'  # Thay thế bằng một khóa bí mật thực sự

# Đăng ký các Blueprint
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(brand_bp, url_prefix="/brand")
app.register_blueprint(campaign_bp, url_prefix="/campaign")
app.register_blueprint(notification_bp, url_prefix="/notification")
app.register_blueprint(transaction_bp, url_prefix="/transaction")
app.register_blueprint(point_bp, url_prefix="/point")
app.register_blueprint(voucher_bp, url_prefix="/voucher")



# Route gốc
@app.route('/')
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
