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
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s AND status = 1", (username, password))
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
        return jsonify({"success": True, "role": "brand", "redirect": f"/user/brand?user_id={user_id}&username={username}&brand_id={brand['brand_id']}"})

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
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT membertype FROM customer WHERE user_id = %s", (user_id,))
    customer = cursor.fetchone()
    conn.close()
    # Map membertype to membership name
    membertype_map = {
        1: 'Thành viên Bạc',
        2: 'Thành viên Vàng',
        3: 'Thành viên Kim cương'
    }
    if customer and customer['membertype'] in membertype_map:
        membership = membertype_map[customer['membertype']]
    else:
        membership = 'Thành viên'
    return render_template("customer.html", user={"user_id": user_id, "user_name": user_name, "membership": membership})
@user_bp.route('/brand')
def brand_page():
    user_id = request.args.get('user_id')
    user_name = request.args.get('username')
    brand_id = request.args.get('brand_id')
    # user_name = session.get('user_name', '')

    if not user_id:
        return jsonify({"error": "Thiếu user_id"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT brand_id FROM brand WHERE user_id = %s", (user_id,))
    brand = cursor.fetchone()
    conn.close()

    if not brand:
        return jsonify({"error": "Không tìm thấy thương hiệu cho user_id này"}), 404

    return render_template("brand.html", user={"user_id": user_id, "user_name": user_name, "brand_id": brand_id})

@user_bp.route('/mall')
def mall_page():
    data = request.args
    user_id = data.get('user_id')
    user_name = data.get('username')
    return render_template("mall.html", user={"user_id": user_id, "user_name": user_name})

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

@user_bp.route('/manage_account', methods=['GET'])
def manage_account():
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    return render_template("user_service/mall_manage_account.html", user={"user_id": user_id, "user_name": user_name})

@user_bp.route('/account_customer', methods=['GET'])
def account_customer():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users join user_profile on users.user_id = user_profile.user_id join customer on users.user_id = customer.user_id")
    user = cursor.fetchall()
    conn.close()
    return jsonify({"user": user}), 200

@user_bp.route('/account_brand', methods=['GET'])
def account_brand():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users join user_profile on users.user_id = user_profile.user_id join brand on users.user_id = brand.user_id")
    user = cursor.fetchall()
    conn.close()
    return jsonify({"user": user}), 200

@user_bp.route('/account_mall', methods=['GET'])
def account_mall():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users join user_profile on users.user_id = user_profile.user_id join mall on users.user_id = mall.user_id")
    user = cursor.fetchall()
    conn.close()
    return jsonify({"user": user}), 200

@user_bp.route('/update_status/<int:user_id>/<int:status>', methods=['POST'])
def update_status(user_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET status = %s WHERE user_id = %s", (status, user_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Cập nhật trạng thái thành công!"}), 200

# Lấy thông tin user theo ID
@user_bp.route('/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"success": True, "user": user}), 200
    else:
        return jsonify({"success": False, "message": "Không tìm thấy người dùng!"}), 404
    
# Đếm số lượng user
@user_bp.route('/count_user', methods=['GET'])
def count_user():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as count FROM users join customer on users.user_id = customer.user_id")
    count = cursor.fetchone()
    conn.close()

    if count:
        return jsonify({"success": True, "count": count['count']}), 200
    else:
        return jsonify({"success": False, "message": "Không tìm thấy người dùng!"}), 404

# Đếm số lượng admin
@user_bp.route('/count_admin', methods=['GET'])
def count_admin():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as count FROM users join mall on users.user_id = mall.user_id")
    count = cursor.fetchone()
    conn.close()

    if count:
        return jsonify({"success": True, "count": count['count']}), 200
    else:
        return jsonify({"success": False, "message": "Không tìm thấy người dùng!"}), 404

# Đếm tổng số lượng tài khoản
@user_bp.route('/count_total', methods=['GET'])
def count_total():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as count FROM users")
    count = cursor.fetchone()
    conn.close()

    if count:
        return jsonify({"success": True, "count": count['count']}), 200
    else:
        return jsonify({"success": False, "message": "Không tìm thấy người dùng!"}), 404

# Quản lý brand
@user_bp.route('/manage_brand', methods=['GET'])
def manage_brand():
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    return render_template("user_service/manage_brand.html", user={"user_id": user_id, "user_name": user_name})

# Quản lý điểm
@user_bp.route('/manage_point', methods=['GET'])
def manage_point():
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    return render_template("user_service/manage_point.html", user={"user_id": user_id, "user_name": user_name})

# Quản lý chiến dịch
@user_bp.route('/manage_campaign', methods=['GET'])
def manage_campaign():
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    return render_template("user_service/manage_campaign.html", user={"user_id": user_id, "user_name": user_name})

# Quản lý ưu đãi
@user_bp.route('/manage_discount', methods=['GET'])
def manage_discount():
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    return render_template("user_service/manage_discount.html", user={"user_id": user_id, "user_name": user_name})

# Quản lý thông báo
@user_bp.route('/manage_notification', methods=['GET'])
def manage_notification():
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    return render_template("user_service/manage_notification.html", user={"user_id": user_id, "user_name": user_name})

# Báo cáo
@user_bp.route('/report', methods=['GET'])
def report():
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    return render_template("user_service/report.html", user={"user_id": user_id, "user_name": user_name})

@user_bp.route('/get_customers/<int:brand_id>', methods=['GET'])
def get_customers(brand_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT up.user_id, up.fullname AS name, 
                   CONCAT('KH-', LPAD(up.user_id, 3, '0')) AS customer_code, 
                   up.phone, 
                   COALESCE(pw.total_points, 0) AS total_points, 
                   DATE_FORMAT(t.max_date, '%d/%m/%Y') AS last_transaction_date,
                   CASE 
                       WHEN c.membertype = 3 THEN 'Kim cương'
                       WHEN c.membertype = 2 THEN 'Vàng'
                       WHEN c.membertype = 1 THEN 'Bạc'
                       ELSE 'Đồng'
                   END AS tier
            FROM user_profile up
            JOIN customer c ON up.user_id = c.user_id
            LEFT JOIN point_service.pointwallet pw ON up.user_id = pw.user_id
            LEFT JOIN (
                SELECT user_id, MAX(created_at) AS max_date
                FROM point_service.transactions
                WHERE brand_id = %s
                GROUP BY user_id
            ) t ON up.user_id = t.user_id
            WHERE up.user_id IN (
                SELECT DISTINCT user_id 
                FROM point_service.transactions 
                WHERE brand_id = %s
            )
            LIMIT 4 -- Match dashboard pagination
        """, (brand_id, brand_id))
        customers = cursor.fetchall()
        cursor.close()
        conn.close()
        if not customers:
            return jsonify({"error": "No customers found"}), 404
        return jsonify({"customers": customers}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@user_bp.route('/get_total_customers/<int:brand_id>', methods=['GET'])
def get_total_customers(brand_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT COUNT(DISTINCT t.user_id) AS total_customers
            FROM point_service.transactions t
            WHERE t.brand_id = %s
        """, (brand_id,))
        total_customers = cursor.fetchone()['total_customers']
        cursor.close()
        conn.close()
        return jsonify({"total_customers": total_customers}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    
@user_bp.route('/top_user_chart', methods=['GET'])
def top_user_chart():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT username, pw.total_points
            FROM users u
            JOIN point_service.pointwallet pw ON u.user_id = pw.user_id
            WHERE u.status = 1
            ORDER BY pw.total_points DESC
            LIMIT 3
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        labels = [row['username'] for row in results]
        values = [row['total_points'] for row in results]
        return jsonify({"labels": labels, "values": values}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500