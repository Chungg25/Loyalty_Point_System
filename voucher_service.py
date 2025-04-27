from flask import request, jsonify, Blueprint, render_template
import mysql.connector
from flask_cors import CORS
from datetime import datetime

voucher_bp = Blueprint("voucher", __name__, template_folder='templates')
CORS(voucher_bp)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="voucher_service"
    )

# 1. Tạo voucher
@voucher_bp.route('/vouchers', methods=['POST'])
def create_voucher():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO Voucher (brand_id, title, description, points_required, discount_amount, created_at, start_at, end_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data.get('brand_id'), data['title'], data['description'],
            data['points_required'], data['discount_amount'], datetime.now(),
            data['start_at'], data['end_at']
        ))
        conn.commit()
        return jsonify({"message": "Voucher created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 2. Cập nhật voucher
@voucher_bp.route('/vouchers/<int:voucher_id>', methods=['PUT'])
def update_voucher(voucher_id):
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        UPDATE Voucher SET title=%s, description=%s, points_required=%s,
        discount_amount=%s, start_at=%s, end_at=%s
        WHERE voucher_id=%s
        """

        cursor.execute(query, (
            data['title'], data['description'], data['points_required'],
            data['discount_amount'], data['start_at'], data['end_at'], voucher_id
        ))
        conn.commit()
        return jsonify({"message": "Voucher updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 3. Xóa voucher
@voucher_bp.route('/vouchers/<int:voucher_id>', methods=['DELETE'])
def delete_voucher(voucher_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Kiểm tra xem voucher có tồn tại không
        cursor.execute("SELECT * FROM Voucher WHERE voucher_id = %s", (voucher_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "Voucher không tồn tại."}), 404

        # Xóa voucher
        cursor.execute("DELETE FROM Voucher WHERE voucher_id = %s", (voucher_id,))
        conn.commit()

        return jsonify({"message": "Voucher đã được xóa thành công."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 4. Lấy chi tiết voucher
@voucher_bp.route('/vouchers/<int:voucher_id>', methods=['GET'])
def get_voucher(voucher_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Voucher WHERE voucher_id=%s", (voucher_id,))
        voucher = cursor.fetchone()
        return jsonify(voucher)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 5. Lọc danh sách voucher
@voucher_bp.route('/vouchers', methods=['GET'])
def list_vouchers():
    brand_id = request.args.get('brand_id')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Voucher WHERE 1=1"
        params = []
        if brand_id:
            query += " AND brand_id = %s"
            params.append(brand_id)

        cursor.execute(query, tuple(params))
        result = cursor.fetchall()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 6. Đổi voucher
@voucher_bp.route('/vouchers/<int:voucher_id>/redeem', methods=['POST'])
def redeem_voucher(voucher_id):
    data = request.json
    user_id = data.get('user_id')
    points_spent = data.get('points_spent')
    redemption_code = data.get('redemption_code')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO Voucher_Redemption (voucher_id, user_id, points_spent, redeemed_at, redemption_code)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (voucher_id, user_id, points_spent, datetime.now(), redemption_code))
        conn.commit()
        return jsonify({"message": "Voucher redeemed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@voucher_bp.route('/get_rewards/<int:brand_id>', methods=['GET'])
def get_rewards(brand_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                voucher_id AS reward_id, 
                title AS name, 
                description, 
                points_required AS points, 
                discount_amount AS discount,
                start_at AS start_time, 
                end_at AS end_time,
                CASE 
                    WHEN NOW() BETWEEN start_at AND end_at THEN 'Đang hoạt động'
                    ELSE 'Hết hạn'
                END AS status,
                stock ,
                initial_stock   
            FROM voucher
            WHERE brand_id = %s
        """, (brand_id,))
        rewards = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rewards:
            return jsonify({"error": "No rewards found"}), 404
        return jsonify({"rewards": rewards}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@voucher_bp.route('/get_reward_chart/<int:brand_id>', methods=['GET'])
def get_reward_chart(brand_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.title AS name, 
                   COUNT(vr.redemption_id) AS redeemed
            FROM voucher v
            LEFT JOIN voucher_redemption vr ON v.voucher_id = vr.voucher_id
            WHERE v.brand_id = %s
            GROUP BY v.voucher_id, v.title
            ORDER BY redeemed DESC LIMIT 5
        """, (brand_id,))
        reward_data = cursor.fetchall()
        cursor.close()
        conn.close()

        reward_labels = [r['name'] for r in reward_data]
        reward_redeemed = [r['redeemed'] for r in reward_data]

        return jsonify({
            "reward_chart": {
                "labels": reward_labels,
                "data": reward_redeemed
            }
        }), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    
@voucher_bp.route('/get_rewards_redeemed/<int:brand_id>', methods=['GET'])
def get_rewards_redeemed(brand_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS rewards_redeemed FROM voucher_redemption WHERE voucher_id IN (SELECT voucher_id FROM voucher WHERE brand_id = %s)", (brand_id,))
        rewards_redeemed = cursor.fetchone()['rewards_redeemed']
        cursor.close()
        conn.close()
        return jsonify({"rewards_redeemed": rewards_redeemed}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    
@voucher_bp.route('/<int:user_id>/redeemed_vouchers', methods=['GET'])
def get_user_redeemed_vouchers(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT v.*, vr.redeemed_at, vr.points_spent, vr.redemption_code
            FROM Voucher v
            JOIN Voucher_Redemption vr ON v.voucher_id = vr.voucher_id
            WHERE vr.user_id = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()