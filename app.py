from flask import Flask, render_template, jsonify
from flask_cors import CORS
from user_service import user_bp
# from shared import orderNote


app = Flask(__name__)
CORS(app)

app.secret_key = 'abc'  # Thay thế bằng một khóa bí mật thực sự

# Đăng ký các Blueprint
app.register_blueprint(user_bp, url_prefix="/user")
# app.register_blueprint(payment_bp, url_prefix="/payment")
# app.register_blueprint(order_bp, url_prefix="/order")

# Route gốc
@app.route('/')
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
