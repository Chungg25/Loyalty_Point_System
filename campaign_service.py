from flask import request, jsonify, Blueprint, render_template, redirect
import mysql.connector
from flask_cors import CORS
from datetime import datetime

campaign_bp = Blueprint("campaign", __name__, template_folder='templates')
CORS(campaign_bp)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="campaign_service"
    )

# 1. Tạo campaign
@campaign_bp.route('/campaigns', methods=['POST'])
def create_campaign():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO Campaign (brand_id, title, description, points_required, reward, created_at, start_at, end_at, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'DRAFT')
        """
        cursor.execute(query, (
            data['brand_id'], data['title'], data['description'],
            data['points_required'], data['reward'], datetime.now(),
            data['start_at'], data['end_at']
        ))
        conn.commit()
        return jsonify({"message": "Campaign created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 2. Cập nhật campaign
@campaign_bp.route('/campaigns/<int:campaign_id>', methods=['PUT'])
def update_campaign(campaign_id):
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        UPDATE Campaign SET title=%s, description=%s, points_required=%s,
        reward=%s, start_at=%s, end_at=%s
        WHERE campaign_id=%s AND status='DRAFT'
        """
        cursor.execute(query, (
            data['title'], data['description'], data['points_required'],
            data['reward'], data['start_at'], data['end_at'], campaign_id
        ))
        conn.commit()
        return jsonify({"message": "Campaign updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 3. Submit campaign (brand gửi duyệt)
@campaign_bp.route('/campaigns/<int:campaign_id>/submit', methods=['POST'])
def submit_campaign(campaign_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Campaign SET status='PENDING_APPROVAL' WHERE campaign_id=%s AND status='DRAFT'", (campaign_id,))
        conn.commit()
        return jsonify({"message": "Campaign submitted for approval"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 4. MALL: duyệt hoặc từ chối
@campaign_bp.route('/campaigns/<int:campaign_id>/review', methods=['POST'])
def review_campaign(campaign_id):
    data = request.json
    decision = data.get('decision')
    comment = data.get('comment', '')

    if decision not in ['APPROVED', 'REJECTED']:
        return jsonify({"error": "Invalid decision"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Campaign SET status=%s, approval_comment=%s WHERE campaign_id=%s AND status='PENDING_APPROVAL'",
            (decision, comment, campaign_id)
        )
        conn.commit()
        return jsonify({"message": f"Campaign {decision.lower()} successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 5. Lấy chi tiết campaign
@campaign_bp.route('/campaigns/<int:campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Campaign WHERE campaign_id=%s", (campaign_id,))
        campaign = cursor.fetchone()
        return jsonify(campaign)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 6. Lọc danh sách campaign
@campaign_bp.route('/campaigns', methods=['GET'])
def list_campaigns():
    brand_id = request.args.get('brand_id')
    status = request.args.get('status')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Campaign WHERE 1=1"
        params = []
        if brand_id:
            query += " AND brand_id = %s"
            params.append(brand_id)
        if status:
            query += " AND status = %s"
            params.append(status)

        cursor.execute(query, tuple(params))
        result = cursor.fetchall()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 7. Đổi quà (redeem)
@campaign_bp.route('/campaigns/<int:campaign_id>/redeem', methods=['POST'])
def redeem_campaign(campaign_id):
    data = request.json
    user_id = data.get('user_id')
    points_spent = data.get('points_spent')
    redemption_code = data.get('redemption_code')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO Campaign_Redemption (campaign_id, user_id, points_spent, redeemed_at, redemption_code)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (campaign_id, user_id, points_spent, datetime.now(), redemption_code))
        conn.commit()
        return jsonify({"message": "Campaign redeemed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 8. Danh sách redeem theo campaign
@campaign_bp.route('/campaigns/<int:campaign_id>/redemptions', methods=['GET'])
def get_campaign_redemptions(campaign_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Campaign_Redemption WHERE campaign_id=%s", (campaign_id,))
        result = cursor.fetchall()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 9. Danh sách redeemed campaign của user
@campaign_bp.route('/users/<int:user_id>/redeemed-campaigns', methods=['GET'])
def get_user_redeemed_campaigns(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT c.*, cr.redeemed_at, cr.points_spent
        FROM Campaign c
        JOIN Campaign_Redemption cr ON c.campaign_id = cr.campaign_id
        WHERE cr.user_id = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 10. Giao diện: Review campaign form
@campaign_bp.route('/campaigns/<int:campaign_id>/review_form', methods=['GET', 'POST'])
def review_campaign_form(campaign_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        decision = request.form.get('decision')
        comment = request.form.get('comment')
        if decision not in ['APPROVED', 'REJECTED']:
            return "Lựa chọn không hợp lệ", 400
        try:
            cursor.execute(
                "UPDATE Campaign SET status=%s, approval_comment=%s WHERE campaign_id=%s AND status='PENDING_APPROVAL'",
                (decision, comment, campaign_id)
            )
            conn.commit()
            return f"Chiến dịch đã được {decision.lower()}.", 200
        except Exception as e:
            return f"Lỗi: {e}", 500

    cursor.execute("SELECT * FROM Campaign WHERE campaign_id=%s", (campaign_id,))
    campaign = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("campaign_service/review_campaign.html", campaign=campaign)

# 11. Giao diện: Danh sách campaign đang chờ duyệt
@campaign_bp.route('/campaigns/pending/list', methods=['GET'])
def pending_campaign_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Campaign WHERE status = 'PENDING_APPROVAL'")
    campaigns = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("campaign_service/pending_campaign_list.html", campaigns=campaigns)


