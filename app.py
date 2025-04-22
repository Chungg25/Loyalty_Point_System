from flask import Flask, render_template, jsonify
from flask_cors import CORS
from user_service import user_bp
from brand_service import brand_bp
from campaign_service import campaign_bp


app = Flask(__name__)
CORS(app)

app.secret_key = 'abc'  # Thay thế bằng một khóa bí mật thực sự

# Đăng ký các Blueprint
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(brand_bp, url_prefix="/brand")
app.register_blueprint(campaign_bp, url_prefix="/campaign")

# Route gốc
@app.route('/')
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
