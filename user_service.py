from flask import Flask, render_template, request, jsonify, Blueprint, render_template
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

@user_bp.route('/login', methods=['GET'])
def login_page():
    return render_template("login.html")

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
    conn.close()

    if user:
        return jsonify({"success": True, "message": "Đăng nhập thành công!", "user": user}), 200
    else:
        return jsonify({"success": False, "message": "Tên đăng nhập hoặc mật khẩu không đúng!"}), 401
    
@user_bp.route('/customer', methods=['GET'])
def customer_page():
    user_id = request.args.get('user_id')
    user_name = request.args.get('username')
    return render_template("/user_service/customer.html", user={"user_id": user_id, "user_name": user_name})

@user_bp.route('/brand', methods=['GET'])
def brand_page():
    user_id = request.args.get('user_id')
    user_name = request.args.get('username')
    return render_template("/user_service/brand.html", user={"user_id": user_id, "user_name": user_name})

@user_bp.route('/mall', methods=['GET'])
def mall_page():
    user_id = request.args.get('user_id')
    user_name = request.args.get('username')
    return render_template("/user_service/mall.html", user={"user_id": user_id, "user_name": user_name})

@user_bp.route('/infor', methods=['POST'])
def infor():
    user_id = request.args.get('user_id')

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
    return render_template('login.html')