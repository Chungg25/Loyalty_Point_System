from flask import request, jsonify, Blueprint, render_template, redirect
import mysql.connector
from flask_cors import CORS
from datetime import datetime
import random
import string
import requests

point_bp = Blueprint("point", __name__, template_folder='templates')
CORS(point_bp)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="point_service"
    )

# def get_db_connection():
#     return mysql.connector.connect(
#         host="han312.mysql.pythonanywhere-services.com",
#         user="han312",
#         password="SOA2025@",
#         database= "han312$point_service"
#     )

@point_bp.route('/get_total_points/<int:brand_id>', methods=['GET'])
def get_total_points(brand_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT SUM(pl.points) AS total_points
            FROM Point_Log pl
            WHERE pl.type = 'EARN'
              AND pl.source_type = 'TRANSACTION'
              AND pl.brand_id = %s
        """, (brand_id,))
        result = cursor.fetchone()
        total_points = result['total_points'] or 0

        cursor.close()
        conn.close()

        return jsonify({"total_points": total_points}), 200

    except mysql.connector.Error as err:
        print(f"Error fetching total points: {err}")
        return jsonify({"error": str(err)}), 500

@point_bp.route('/get_user_points/<int:user_id>', methods=['GET'])
def get_user_points(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Lấy tổng điểm của người dùng từ bảng PointWallet
        cursor.execute("SELECT total_points FROM PointWallet WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            return jsonify({"error": "Người dùng không có ví điểm!"}), 404

        total_points = result['total_points'] or 0

        cursor.close()
        conn.close()

        return jsonify({"total_points": total_points}), 200

    except mysql.connector.Error as err:
        print(f"Error fetching user points: {err}")
        return jsonify({"error": str(err)}), 500

@point_bp.route('/redeem_points', methods=['POST'])
def redeem_points():
    try:
        # Lấy dữ liệu từ request
        data = request.get_json()
        required_fields = ['user_id', 'points_required', 'campaign_id', 'description']

        # Kiểm tra các trường bắt buộc
        for field in required_fields:
            if field not in data or data[field] is None:
                return jsonify({"error": f"Thiếu trường bắt buộc: {field}"}), 400

        user_id = int(data['user_id'])
        points_required = int(data['points_required'])
        campaign_id = int(data['campaign_id'])
        description = data['description']

        # Kết nối database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Kiểm tra và trừ điểm trong PointWallet
        cursor.execute("SELECT point_wallet_id, total_points FROM PointWallet WHERE user_id = %s", (user_id,))
        wallet = cursor.fetchone()
        if not wallet or wallet['total_points'] < points_required:
            cursor.close()
            conn.close()
            return jsonify({"error": "Không đủ điểm để đổi quà!"}), 400

        new_total = wallet['total_points'] - points_required
        cursor.execute("UPDATE PointWallet SET total_points = %s, last_update = NOW() WHERE point_wallet_id = %s",
                       (new_total, wallet['point_wallet_id']))

        # Ghi log vào Point_Log
        cursor.execute("""
            INSERT INTO Point_Log (point_wallet_id, type, source_type, source_id, points, metadata, description, created_at)
            VALUES (%s, 'REDEEM', 'CAMPAIGN', %s, %s, NULL, %s, NOW())
        """, (wallet['point_wallet_id'], campaign_id, points_required, description))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Điểm đã được trừ thành công!",
            "remaining_points": new_total
        }), 200

    except mysql.connector.Error as err:
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()
        return jsonify({"error": str(err)}), 500
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()
        return jsonify({"error": str(e)}), 500

@point_bp.route('/redeem_points_by_voucher', methods=['POST'])
def redeem_points_by_voucher():
    try:
        # Lấy dữ liệu từ request
        data = request.get_json()
        required_fields = ['user_id', 'points_required', 'voucher_id', 'description']

        # Kiểm tra các trường bắt buộc
        for field in required_fields:
            if field not in data or data[field] is None:
                return jsonify({"error": f"Thiếu trường bắt buộc: {field}"}), 400

        user_id = int(data['user_id'])
        points_required = int(data['points_required'])
        voucher_id = int(data['voucher_id'])
        description = data['description']

        # Kết nối database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Kiểm tra và trừ điểm trong PointWallet
        cursor.execute("SELECT point_wallet_id, total_points FROM PointWallet WHERE user_id = %s", (user_id,))
        wallet = cursor.fetchone()
        if not wallet or wallet['total_points'] < points_required:
            cursor.close()
            conn.close()
            return jsonify({"error": "Không đủ điểm để đổi quà!"}), 400

        new_total = wallet['total_points'] - points_required
        cursor.execute("UPDATE PointWallet SET total_points = %s, last_update = NOW() WHERE point_wallet_id = %s",
                       (new_total, wallet['point_wallet_id']))

        # Ghi log vào Point_Log với source_type='VOUCHER' và source_id=voucher_id
        cursor.execute("""
            INSERT INTO Point_Log (point_wallet_id, type, source_type, source_id, points, metadata, description, created_at)
            VALUES (%s, 'REDEEM', 'VOUCHER', %s, %s, NULL, %s, NOW())
        """, (wallet['point_wallet_id'], voucher_id, points_required, description))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Điểm đã được trừ thành công!",
            "remaining_points": new_total
        }), 200

    except mysql.connector.Error as err:
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()
        return jsonify({"error": str(err)}), 500
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()
        return jsonify({"error": str(e)}), 500
    
@point_bp.route('/get_points/<int:user_id>', methods=['GET'])
def get_points(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT total_points from PointWallet where user_id = %s
        """, (user_id,))
        points = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(points), 200

    except mysql.connector.Error as err:
        print(f"Error fetching points: {err}")
        return jsonify({"error": str(err)}), 500

@point_bp.route('/get_payments', methods=['GET'])
def get_payments():
    try:
        # Lấy tham số từ query string
        brand_id = request.args.get('brand_id', type=int)
        page = request.args.get('page', default=1, type=int)
        items_per_page = request.args.get('items_per_page', default=10, type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        status = request.args.get('status')

        print(f"Received request: brand_id={brand_id}, page={page}, items_per_page={items_per_page}, start_date={start_date}, end_date={end_date}, status={status}")

        if not brand_id:
            return jsonify({"error": "Thiếu brand_id"}), 400
        if page < 1 or items_per_page < 1:
            return jsonify({"error": "page và items_per_page phải lớn hơn 0"}), 400

        # Tính offset cho phân trang
        offset = (page - 1) * items_per_page

        # Kết nối database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Xây dựng truy vấn đếm tổng số giao dịch
        count_query = """
            SELECT COUNT(*) AS total
            FROM Transactions t
            WHERE t.brand_id = %s
        """
        params = [brand_id]
        if start_date:
            count_query += " AND t.created_at >= %s"
            params.append(start_date)
        if end_date:
            count_query += " AND t.created_at <= %s"
            params.append(end_date)

        cursor.execute(count_query, params)
        total_payments = cursor.fetchone()['total']

        # Xây dựng truy vấn lấy danh sách giao dịch
        query = """
            SELECT
                t.transaction_id,
                t.invoice_code AS transaction_id,
                us.fullname AS customer_name,
                DATE_FORMAT(t.created_at, '%d/%m/%Y') AS payment_date,
                t.amount,
                COALESCE(pl.points, 0) AS points_earned
            FROM Transactions t 
            JOIN User_Snapshot us ON t.user_snapshot_id = us.user_snapshot_id
            LEFT JOIN Point_Log pl ON pl.source_type = 'TRANSACTION' AND pl.source_id = t.transaction_id AND pl.type = 'EARN'
            WHERE t.brand_id = %s
        """
        params = [brand_id]
        if start_date:
            query += " AND t.created_at >= %s"
            params.append(start_date)
        if end_date:
            query += " AND t.created_at <= %s"
            params.append(end_date)
        query += " ORDER BY t.created_at DESC LIMIT %s OFFSET %s"
        params.extend([items_per_page, offset])

        cursor.execute(query, params)
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        if not results:
            return jsonify({
                "message": "Không có giao dịch nào phù hợp với bộ lọc",
                "payments": [],
                "total_payments": total_payments
            }), 200

        return jsonify({
            "payments": results,
            "total_payments": total_payments
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
    
@point_bp.route('/monthly_revenue', methods=['GET'])
def monthly_vevenue():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT  SUM(t.amount) AS total
            FROM Transactions t
            WHERE MONTH(t.created_at) = MONTH(CURRENT_DATE())
        """)
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        total = result['total'] or 0
        # Format thành chuỗi tiền tệ VND
        formatted_total = "{:,.0f}".format(total)
        return jsonify({"total": formatted_total}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@point_bp.route('/monthly_revenue_chart', methods=['GET'])
def monthly_revenue():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                DATE_FORMAT(t.created_at, '%m/%Y') AS month,
                SUM(t.amount) AS total
            FROM Transactions t
            GROUP BY YEAR(t.created_at), MONTH(t.created_at)
            ORDER BY YEAR(t.created_at) DESC, MONTH(t.created_at) DESC
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        # Trả về mảng các tháng và doanh thu
        months = [row['month'] for row in results]
        totals = [float(row['total']) for row in results]
        return jsonify({"months": months, "totals": totals}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@point_bp.route('/top_brand_chart', methods=['GET'])
def top_brand_chart():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                t.brand_id,
                b.brandname,
                SUM(t.amount) AS total
            FROM Transactions t
            JOIN Brand_Service.Brand b ON t.brand_id = b.brand_id
            GROUP BY t.brand_id, b.brandname
            ORDER BY total DESC
            LIMIT 3
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        # Trả về mảng brand và doanh thu
        brands = [row['brandname'] for row in results]
        totals = [float(row['total']) for row in results]
        return jsonify({"brands": brands, "totals": totals}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@point_bp.route('/total_accumulated_points', methods=['GET'])
def total_accumulated_points():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) AS total_points
            FROM Transactions
            WHERE amount > 0
        """)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({"total_points": result['total_points']}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@point_bp.route('/total_current_points', methods=['GET'])
def total_current_points():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT COALESCE(SUM(total_points), 0) AS total_points
            FROM Pointwallet
        """)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({"total_points": result['total_points']}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@point_bp.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        # Lấy dữ liệu từ request
        data = request.get_json()
        required_fields = ['user_id', 'brand_id', 'invoice_code', 'amount', 'created_at', 'user_snapshot_id']

        # Kiểm tra các trường bắt buộc
        for field in required_fields:
            if field not in data or data[field] is None:
                return jsonify({"error": f"Thiếu trường bắt buộc: {field}"}), 400

        user_id = int(data['user_id'])
        brand_id = int(data['brand_id'])
        invoice_code = data['invoice_code']
        amount = float(data['amount'])
        created_at_str = data['created_at']
        user_snapshot_id = int(data['user_snapshot_id'])

        brand_coefficient = float(data['coefficient'])
        member_coefficient = float(data['member_coefficient'])


        try:
            created_at = datetime.strptime(created_at_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({"error": "Định dạng created_at không hợp lệ, phải là YYYY-MM-DD HH:MM:SS"}), 400

        # Kết nối database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Thêm giao dịch vào bảng Transactions
        cursor.execute("""
            INSERT INTO Transactions (user_id, brand_id, invoice_code, amount, created_at, user_snapshot_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, brand_id, invoice_code, amount, created_at, user_snapshot_id))

        # Lấy transaction_id vừa thêm
        transaction_id = cursor.lastrowid

        # Cập nhật số điểm trong bảng PointWallet
        cursor.execute("""
            SELECT FLOOR(
                %s / cr.rate * %s * %s
            ) AS earned_points
            FROM ConversionRule cr
            WHERE %s BETWEEN cr.effective_from AND IFNULL(cr.effective_to, NOW())
            LIMIT 1
        """, (amount, brand_coefficient, member_coefficient, created_at))
        result = cursor.fetchone()

        # Kiểm tra kết quả truy vấn
        if not result:
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"error": "Không thể tính điểm do thiếu dữ liệu (Brand, Customer, MemberTypeCoefficient, hoặc ConversionRule)!"}), 500

        earned_points = result['earned_points'] or 0

        # Kiểm tra PointWallet tồn tại
        cursor.execute("SELECT point_wallet_id FROM PointWallet WHERE user_id = %s", (user_id,))
        wallet = cursor.fetchone()
        if not wallet:
            cursor.execute("INSERT INTO PointWallet (user_id, total_points, last_update) VALUES (%s, %s, CURRENT_TIMESTAMP)", (user_id, 0))
            point_wallet_id = cursor.lastrowid
        else:
            point_wallet_id = wallet['point_wallet_id']

        # Cập nhật điểm trong PointWallet
        cursor.execute("""
            UPDATE PointWallet
            SET total_points = total_points + %s,
                last_update = CURRENT_TIMESTAMP
            WHERE user_id = %s
        """, (earned_points, user_id))

        # Ghi log tích điểm vào Point_Log
        cursor.execute("""
            INSERT INTO Point_Log (
                point_wallet_id, brand_id, type, source_type, source_id, points, metadata, description, created_at
            ) VALUES (%s, %s, 'EARN', 'TRANSACTION', %s, %s, NULL, %s, CURRENT_TIMESTAMP)
        """, (point_wallet_id, brand_id, transaction_id, earned_points, f'Tích điểm từ hóa đơn {invoice_code}'))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Transaction added successfully", "earned_points": earned_points}), 201

    except mysql.connector.Error as err:
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()
        return jsonify({"error": str(err)}), 500
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()
        return jsonify({"error": str(e)}), 500

@point_bp.route('/transactions', methods=['GET'])
def transactions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * from Transactions
        """)
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        if not transactions:
            return jsonify({"error": "No transactions found"}), 404
        return jsonify({"transactions": transactions}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@point_bp.route('/pointwallet', methods=['GET'])
def pointwallet():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * from PointWallet
        """)
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        if not transactions:
            return jsonify({"error": "No transactions found"}), 404
        return jsonify({"transactions": transactions}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@point_bp.route('/check_invoice', methods=['GET'])
def check_invoice():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        invoice_code = request.args.get('invoice_code')
        cursor.execute("""
            SELECT * from Transactions where invoice_code = %s
        """, (invoice_code,))
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        if not transactions:
            return jsonify({"error": "No transactions found"}), 404
        return jsonify({"transactions": transactions}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    
@point_bp.route('/<int:user_id>/transaction_history', methods=['GET'])
def get_transaction_history(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Truy vấn lấy lịch sử giao dịch từ bảng Point_Log
        query = """
            SELECT
                pl.created_at,
                pl.type,
                pl.source_type,
                pl.source_id,
                pl.points,
                pl.description,
                pl.metadata
            FROM Point_Log pl
            WHERE pl.point_wallet_id = (
                SELECT point_wallet_id FROM PointWallet WHERE user_id = %s
            )
            ORDER BY pl.created_at DESC
        """
        cursor.execute(query, (user_id,))
        transactions = cursor.fetchall()

        cursor.close()
        conn.close()

        if not transactions:
            return jsonify({"message": "Không có giao dịch nào", "transactions": []}), 200

        # Định dạng dữ liệu trả về
        formatted_transactions = []
        for t in transactions:
            # Điều chỉnh số điểm: nếu là REDEEM, trả về số âm
            points = -t['points'] if t['type'] == 'REDEEM' else t['points']
            
            transaction = {
                "date": t['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
                "transaction_id": f"{t['source_type'][:3]}{t['source_id']}",
                "store": "Brand",  # Có thể cần lấy thông tin brand từ bảng Brand nếu cần
                "description": t['description'] or f"{t['type']}: {t['source_type']} {t['source_id']}",
                "points": points,  # Số điểm đã được điều chỉnh (âm cho REDEEM)
                "status": "Hoàn thành",
                "source_type": t['source_type'],
            }
            formatted_transactions.append(transaction)

        return jsonify({"transactions": formatted_transactions}), 200

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