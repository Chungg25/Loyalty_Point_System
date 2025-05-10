from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import mysql.connector
from flask_cors import CORS
from datetime import datetime, timedelta

user_bp = Blueprint("user", __name__)
CORS(user_bp)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="user_service"
    )

# def get_db_connection():
#     return mysql.connector.connect(
#         host="han312.mysql.pythonanywhere-services.com",
#         user="han312",
#         password="SOA2025@",
#         database= "han312$user_service"
#     )

@user_bp.route('/login', methods=['GET'])
def login_page():
    return_url = request.args.get('return_url', '/user/customer')
    return render_template("login.html", return_url=return_url)

@user_bp.route('/transaction_qr', methods=['GET'])
def transaction_qr_page():
    user_id = request.args.get('user_id')
    user_name = request.args.get('username', 'Khách hàng')
    # Kiểm tra đăng nhập và vai trò
    if not user_id:
        return redirect(url_for('user.login_page', return_url=request.url))

    # Lấy dữ liệu từ query string và truyền vào template
    transaction_data = {
        "user_id": user_id,
        "brand_id": request.args.get('brand_id'),
        "invoice_code": request.args.get('invoice_code'),
        "amount": request.args.get('amount'),
        "created_at": request.args.get('created_at'),
    }
    user_snapshot_id = request.args.get('user_snapshot_id')
    return render_template("transaction_qr.html", transaction_data=transaction_data, user_snapshot_id=user_snapshot_id, user_name=user_name)

# Xử lý đăng nhập (POST)
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    return_url = data.get('return_url', None)  # Lấy return_url từ dữ liệu gửi lên

    if not username or not password:
        return jsonify({"success": False, "message": "Thiếu tên đăng nhập hoặc mật khẩu!"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE username = %s AND password = %s AND status = 1", (username, password))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"success": False, "message": "Tên đăng nhập hoặc mật khẩu không đúng!"}), 401

    user_id = user['user_id']
    role = None
    redirect_url = None

    cursor.execute("SELECT * FROM Customer WHERE user_id = %s", (user_id,))
    if cursor.fetchone():
        role = "customer"

    cursor.execute("SELECT brand_id FROM Brand WHERE user_id = %s", (user_id,))
    brand = cursor.fetchone()
    if brand:
        role = "brand"

    cursor.execute("SELECT * FROM Mall WHERE user_id = %s", (user_id,))
    if cursor.fetchone():
        role = "mall"

    conn.close()

    if not role:
        return jsonify({"success": False, "message": "Người dùng không thuộc bất kỳ vai trò nào!"}), 403

    if return_url:
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

        parsed = urlparse(return_url)
        query = parse_qs(parsed.query)
        query['user_id'] = [str(user_id)]
        query['username'] = [username]
        new_query = urlencode(query, doseq=True)
        redirect_url = urlunparse(parsed._replace(query=new_query))
    else:
        if role == "customer":
            redirect_url = f"/user/customer?user_id={user_id}&username={username}"
        elif role == "brand":
            redirect_url = f"/user/brand?user_id={user_id}&username={username}&brand_id={brand['brand_id']}"
        elif role == "mall":
            redirect_url = f"/user/mall?user_id={user_id}&username={username}"

    return jsonify({
        "success": True,
        "role": role,
        "redirect": redirect_url
    })

# Trang tương ứng mỗi vai trò
@user_bp.route('/customer')
def customer_page():
    user_id = request.args.get('user_id')
    user_name = request.args.get('username', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT membertype FROM Customer WHERE user_id = %s", (user_id,))
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

    if not user_id:
        return jsonify({"error": "Thiếu user_id"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT brand_id FROM Brand WHERE user_id = %s", (user_id,))
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
    cursor.execute("SELECT * FROM User_Profile WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"success": True, "message": "Thông tin người dùng", "user": user}), 200
    else:
        return jsonify({"success": False, "message": "Không tìm thấy người dùng!"}), 404

@user_bp.route('/logout')
def logout():
    return redirect(url_for("user.login_page"))

@user_bp.route('/manage_account', methods=['GET'])
def manage_account():
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    return render_template("user_service/mall_manage_account.html", user={"user_id": user_id, "user_name": user_name})

@user_bp.route('/account_customer', methods=['GET'])
def account_customer():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users join User_Profile on Users.user_id = User_Profile.user_id join customer on Users.user_id = customer.user_id")
    user = cursor.fetchall()
    conn.close()
    return jsonify({"user": user}), 200

@user_bp.route('/account_brand', methods=['GET'])
def account_brand():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users join User_Profile on Users.user_id = User_Profile.user_id join Brand on Users.user_id = Brand.user_id")
    user = cursor.fetchall()
    conn.close()
    return jsonify({"user": user}), 200

@user_bp.route('/account_mall', methods=['GET'])
def account_mall():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users join User_Profile on Users.user_id = User_Profile.user_id join Mall on Users.user_id = Mall.user_id")
    user = cursor.fetchall()
    conn.close()
    return jsonify({"user": user}), 200

@user_bp.route('/update_status/<int:user_id>/<int:status>', methods=['POST'])
def update_status(user_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET status = %s WHERE user_id = %s", (status, user_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Cập nhật trạng thái thành công!"}), 200

# Lấy thông tin user theo IDbạn không
@user_bp.route('/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT *
        FROM Users
        JOIN Customer ON Users.user_id = Customer.user_id
        JOIN MemberTypeCoefficient ON Customer.membertype = MemberTypeCoefficient.membertype
        WHERE Users.user_id = %s
    """, (user_id,))
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
    cursor.execute("SELECT COUNT(*) as count FROM Users join Customer on Users.user_id = Customer.user_id")
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
    cursor.execute("SELECT COUNT(*) as count FROM Users join Mall on Users.user_id = Mall.user_id")
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
    cursor.execute("SELECT COUNT(*) as count FROM Users")
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
    return render_template("user_service/report.html")

@user_bp.route('/get_customers', methods=['POST'])
def get_customers():
    try:
        data = request.get_json()
        brand_id = data.get('brand_id')
        page = data.get('page', 1)
        limit = data.get('limit', 10)
        user_points = data.get('user_points', [])  # Danh sách {user_id, total_points}

        if not brand_id:
            return jsonify({"error": "Thiếu brand_id"}), 400
        if page < 1 or limit < 1:
            return jsonify({"error": "page và limit phải lớn hơn 0"}), 400

        offset = (page - 1) * limit

        # Tạo dictionary để tra cứu total_points
        points_dict = {up['user_id']: up['total_points'] for up in user_points}

        # Kết nối cơ sở dữ liệu user_service
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Truy vấn danh sách khách hàng
        cursor.execute("""
            SELECT up.user_id, up.fullname AS name,
                   CONCAT('KH-', LPAD(up.user_id, 3, '0')) AS customer_code,
                   up.phone,
                   c.membertype,
                   c.created_at
            FROM User_Profile up
            JOIN Customer c ON up.user_id = c.user_id
            LIMIT %s OFFSET %s
        """, (limit, offset))
        user_profiles = cursor.fetchall()

        # Đếm tổng số khách hàng
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM User_Profile up
            JOIN Customer c ON up.user_id = c.user_id
        """)
        total_customers = cursor.fetchone()['total']

        # Tính thống kê
        thirty_days_ago = datetime.now() - timedelta(days=30)
        cursor.execute("""
            SELECT COUNT(*) AS new_customers
            FROM Customer c
            WHERE c.created_at >= %s
        """, (thirty_days_ago,))
        new_customers_30d = cursor.fetchone()['new_customers']

        cursor.execute("""
            SELECT COUNT(*) AS vip_customers
            FROM Customer c
            WHERE c.membertype >= 2  -- Giả định Vàng (2) và Kim cương (3) là VIP
        """)
        vip_customers = cursor.fetchone()['vip_customers']

        cursor.close()
        conn.close()

        # Kết hợp dữ liệu khách hàng
        customers = []
        for up in user_profiles:
            uid = up['user_id']
            customers.append({
                "user_id": uid,
                "name": up['name'],
                "customer_code": up['customer_code'],
                "phone": up['phone'],
                "total_points": points_dict.get(uid, 0),  # Lấy total_points từ user_points
                "last_transaction_date": None,  # Không có Transactions, đặt là null
                "tier": (
                    "Kim cương" if up['membertype'] == 3 else
                    "Vàng" if up['membertype'] == 2 else
                    "Bạc" if up['membertype'] == 1 else
                    "Đồng"
                ),
            })

        return jsonify({
            "stats": {
                "total_customers": total_customers,
                "new_customers_30d": new_customers_30d,
                "vip_customers": vip_customers
            },
            "customers": customers,
            "total_customers": total_customers
        }), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        if 'conn' in locals():
            cursor.close()
            conn.close()
        return jsonify({"error": str(err)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        if 'conn' in locals():
            cursor.close()
            conn.close()
        return jsonify({"error": str(e)}), 500


@user_bp.route('/get_total_customers/<int:brand_id>', methods=['POST'])
def get_total_customers(brand_id):
    try:
        data = request.get_json()
        transactions = data.get('transactions', [])

        if not brand_id or not transactions:
            return jsonify({"error": "Thiếu brand_id hoặc transactions"}), 400

        user_ids = {
            t['user_id']
            for t in transactions
            if t.get('brand_id') == brand_id
        }

        return jsonify({"total_customers": len(user_ids)}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/top_user_chart', methods=['GET'])
def top_user_chart():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT username, pw.total_points
            FROM Users u
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

# Lấy hệ số của tất cả các thành viên
@user_bp.route('/get_membertype_coefficients', methods=['GET'])
def get_membertype_coefficients():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM MemberTypeCoefficient join Customer on MemberTypeCoefficient.membertype = Customer.membertype")
        coefficients = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"coefficients": coefficients}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500