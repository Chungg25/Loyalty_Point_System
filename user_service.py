from flask import Blueprint, render_template, request, jsonify, redirect, session, url_for
import mysql.connector
from flask_cors import CORS

user_bp = Blueprint("user", __name__)
CORS(user_bp)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="user_service"
    )

<<<<<<< HEAD
=======
# Trang đăng nhập (GET)
>>>>>>> 7dee5e481f144bf5a1191117fa3f6ee683e28096
@user_bp.route('/login', methods=['GET'])
def login_page():
    return render_template("login.html")

# Xử lý đăng nhập (POST)
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Thiếu tên đăng nhập hoặc mật khẩu!"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"success": False, "message": "Tên đăng nhập hoặc mật khẩu không đúng!"}), 401

    user_id = user['user_id']

    # Kiểm tra vai trò
    cursor.execute("SELECT * FROM customer WHERE user_id = %s", (user_id,))
    if cursor.fetchone():
        conn.close()
        session.clear()
        session['user_id'] = user_id
        session['role'] = 'customer'
        session['user_name'] = username
        return jsonify({"success": True, "role": "customer", "redirect": f"/user/customer?user_id={user_id}&username={username}"})

    cursor.execute("SELECT brand_id FROM brand WHERE user_id = %s", (user_id,))
    brand = cursor.fetchone()
    if brand:
        conn.close()
        session.clear()
        session['user_id'] = user_id
        session['role'] = 'brand'
        session['brand_id'] = brand['brand_id']
        session['user_name'] = username
        return jsonify({"success": True, "role": "brand", "redirect": f"/user/brand?user_id={user_id}&username={username}"})

    cursor.execute("SELECT * FROM mall WHERE user_id = %s", (user_id,))
    if cursor.fetchone():
        conn.close()
        session.clear()
        session['user_id'] = user_id
        session['role'] = 'mall'
        session['user_name'] = username
        return jsonify({"success": True, "role": "mall", "redirect": f"/user/mall?user_id={user_id}&username={username}"})

    conn.close()
    return jsonify({"success": False, "message": "Người dùng không thuộc bất kỳ vai trò nào!"}), 403

# Trang tương ứng mỗi vai trò
@user_bp.route('/customer')
def customer_page():
    user_id = request.args.get('user_id')
    user_name = session.get('user_name', '')
    return render_template("user_service/customer.html", user={"user_id": user_id, "user_name": user_name})

@user_bp.route('/brand')
def brand_page():
    user_id = request.args.get('user_id')
    user_name = session.get('user_name', '')

    if not user_id:
        return jsonify({"error": "Thiếu user_id"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT brand_id FROM brand WHERE user_id = %s", (user_id,))
    brand = cursor.fetchone()
    conn.close()

    if not brand:
        session['brand_id'] = None
        return jsonify({"error": "Không tìm thấy thương hiệu cho user_id này"}), 404

    session['brand_id'] = brand['brand_id']
    return render_template("user_service/brand.html", user={"user_id": user_id, "user_name": user_name, "brand_id": session['brand_id']})

@user_bp.route('/mall')
def mall_page():
    user_id = request.args.get('user_id')
    user_name = session.get('user_name', '')
    return render_template("user_service/mall.html", user={"user_id": user_id, "user_name": user_name})

# API lấy thông tin người dùng
@user_bp.route('/infor', methods=['POST'])
def infor():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Thiếu user_id!"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_profile WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"success": True, "message": "Thông tin người dùng", "user": user}), 200
    else:
        return jsonify({"success": False, "message": "Không tìm thấy người dùng!"}), 404

@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("user.login_page"))

# Debug session (tùy chọn, xóa khi production)
@user_bp.route('/debug_session')
def debug_session():
    return jsonify(dict(session))