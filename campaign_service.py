from flask import request, jsonify, Blueprint, render_template, redirect, session
import mysql.connector
from flask_cors import CORS
from datetime import datetime
import random
import string

campaign_bp = Blueprint("campaign", __name__, template_folder='templates')
CORS(campaign_bp)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="campaign_service"
    )

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@campaign_bp.route('/create_campaign', methods=['GET'])
def create_campaign_page():
    if 'brand_id' not in session:
        return redirect('/user/login')
    user_name = session.get('user_name', '')  # Sửa lại key này cho đúng
    return render_template("campaign_service/create_campaign.html", user_name=user_name, brand_id=session['brand_id'])
@campaign_bp.route('/campaigns', methods=['POST'])
def create_campaign():
    if 'brand_id' not in session or not session['brand_id']:
        return jsonify({"error": "Bạn chưa đăng nhập hoặc không có quyền tạo chiến dịch."}), 401

    brand_id = session['brand_id']
    data = request.json
    required_fields = ['title', 'description', 'points_required', 'reward', 'start_at', 'end_at']
    for field in required_fields:
        if field not in data or isinstance(data[field], list):
            return jsonify({"error": f"Thiếu hoặc sai kiểu dữ liệu trường: {field}"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        while True:
            redemption_code = generate_code()
            cursor.execute("SELECT campaign_id FROM Campaign WHERE redemption_code = %s LIMIT 1", (redemption_code,))
            if not cursor.fetchone():
                break

        query = """
        INSERT INTO Campaign (brand_id, title, description, points_required, reward, created_at, start_at, end_at, status, redemption_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'DRAFT', %s)
        """
        cursor.execute(query, (
            brand_id,
            data['title'],
            data['description'],
            int(data['points_required']),
            data['reward'],
            datetime.now(),
            datetime.strptime(data['start_at'], '%Y-%m-%dT%H:%M'),
            datetime.strptime(data['end_at'], '%Y-%m-%dT%H:%M'),
            redemption_code
        ))
        campaign_id = cursor.lastrowid
        conn.commit()
        return jsonify({
            "message": "Tạo chiến dịch thành công!",
            "campaign_id": campaign_id,
            "redemption_code": redemption_code
        }), 201
    except ValueError as ve:
        return jsonify({"error": f"Invalid date format: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi tạo: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

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
            data['title'],
            data['description'],
            data['points_required'],
            data['reward'],
            datetime.strptime(data['start_at'], '%Y-%m-%dT%H:%M'),
            datetime.strptime(data['end_at'], '%Y-%m-%dT%H:%M'),
            campaign_id
        ))
        if cursor.rowcount == 0:
            return jsonify({"error": "Campaign not found or not in DRAFT status"}), 400
        conn.commit()
        return jsonify({"message": "Campaign updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@campaign_bp.route('/campaigns/<int:campaign_id>/submit', methods=['POST'])
def submit_campaign(campaign_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Campaign SET status='PENDING_APPROVAL' WHERE campaign_id=%s AND status='DRAFT'", (campaign_id,))
        if cursor.rowcount == 0:
            return jsonify({"error": "Campaign not found or not in DRAFT status"}), 400
        conn.commit()
        return jsonify({"message": "Campaign submitted for approval"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

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
        if cursor.rowcount == 0:
            return jsonify({"error": "Campaign not found or not in PENDING_APPROVAL status"}), 400
        conn.commit()
        return jsonify({"message": f"Campaign {decision.lower()} successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@campaign_bp.route('/campaigns/<int:campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Campaign WHERE campaign_id=%s", (campaign_id,))
        campaign = cursor.fetchone()
        if not campaign:
            return jsonify({"error": "Campaign not found"}), 404
        return jsonify(campaign)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

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

@campaign_bp.route('/campaigns/<int:campaign_id>/redeem', methods=['POST'])
def redeem_campaign(campaign_id):
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT points_required, redemption_code FROM Campaign WHERE campaign_id = %s", (campaign_id,))
        campaign = cursor.fetchone()
        if not campaign:
            return jsonify({"error": "Campaign not found"}), 404

        points_required = campaign['points_required']
        redemption_code = campaign['redemption_code']

        cursor.execute("SELECT point_wallet_id, total_points FROM Point_Service.PointWallet WHERE user_id = %s", (user_id,))
        wallet = cursor.fetchone()
        if not wallet or wallet['total_points'] < points_required:
            return jsonify({"error": "Not enough points"}), 400

        new_total = wallet['total_points'] - points_required
        cursor.execute("UPDATE Point_Service.PointWallet SET total_points = %s, last_update = NOW() WHERE point_wallet_id = %s",
                       (new_total, wallet['point_wallet_id']))

        cursor.execute("""
            INSERT INTO Campaign_Redemption (campaign_id, user_id, points_spent, redeemed_at)
            VALUES (%s, %s, %s, %s)
        """, (campaign_id, user_id, points_required, datetime.now()))

        cursor.execute("""
        INSERT INTO Point_Service.Point_Log (point_wallet_id, type, source_type, source_id, points, metadata, description, created_at)
        VALUES (%s, 'REDEEM', 'CAMPAIGN', %s, %s, NULL, %s, NOW())
        """, (
            wallet['point_wallet_id'],
            campaign_id,
            points_required,
            f'Đổi quà từ campaign {campaign_id}'
        ))

        conn.commit()
        return jsonify({
            "message": "Redeem thành công!",
            "campaign_id": campaign_id,
            "user_id": user_id,
            "redemption_code": redemption_code,
            "remaining_points": new_total
        })
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@campaign_bp.route('/campaigns/<int:campaign_id>/redemptions', methods=['GET'])
def get_campaign_redemptions(campaign_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT campaign_id, user_id, points_spent, redeemed_at FROM Campaign_Redemption WHERE campaign_id=%s", (campaign_id,))
        result = cursor.fetchall()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

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
            if cursor.rowcount == 0:
                return "Chiến dịch không tồn tại hoặc không ở trạng thái PENDING_APPROVAL", 400
            conn.commit()
            return f"Chiến dịch đã được {decision.lower()}.", 200
        except Exception as e:
            return f"Lỗi: {e}", 500

    cursor.execute("SELECT * FROM Campaign WHERE campaign_id=%s", (campaign_id,))
    campaign = cursor.fetchone()
    if not campaign:
        return "Chiến dịch không tồn tại", 404
    cursor.close()
    conn.close()
    return render_template("campaign_service/review_campaign.html", campaign=campaign)

@campaign_bp.route('/campaigns/pending/list', methods=['GET'])
def pending_campaign_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Campaign WHERE status = 'PENDING_APPROVAL'")
    campaigns = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("campaign_service/pending_campaign_list.html", campaigns=campaigns)

@campaign_bp.route('/campaigns/insights')
def campaign_insights():
    brand = request.args.get('brand')
    from_date = request.args.get('from')
    to_date = request.args.get('to')

    query = """
        SELECT 
            c.title,
            b.brandname,
            COUNT(r.campaign_redemption_id) AS total_redeem,
            SUM(r.points_spent) AS total_points
        FROM Campaign c
        JOIN Brand_Service.Brand b ON c.brand_id = b.brand_id
        LEFT JOIN Campaign_Redemption r ON c.campaign_id = r.campaign_id
    """
    filters = []
    params = []

    if brand:
        filters.append("b.brandname = %s")
        params.append(brand)
    if from_date:
        filters.append("r.redeemed_at >= %s")
        params.append(from_date)
    if to_date:
        filters.append("r.redeemed_at <= %s")
        params.append(to_date)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " GROUP BY c.campaign_id, c.title, b.brandname"

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        insights = []
        for row in rows:
            level = 'low'
            if row['total_redeem'] >= 10:
                level = 'high'
                msg = f" '{row['title']}' của {row['brandname']} rất hiệu quả."
                detail = f"{row['total_redeem']} lượt đổi, {row['total_points'] or 0} điểm tiêu."
            elif row['total_redeem'] >= 1:
                level = 'medium'
                msg = f"'{row['title']}' có tương tác trung bình."
                detail = f"{row['total_redeem']} lượt đổi."
            else:
                msg = f" '{row['title']}' chưa có lượt đổi."
                detail = "Cần xem xét nội dung hoặc quảng bá."

            insights.append({
                "title": row['title'],
                "total_redeem": row['total_redeem'] or 0,
                "level": level,
                "message": msg,
                "detail": detail
            })

        return jsonify(insights)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@campaign_bp.route('/campaigns/dashboard')
def campaign_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS total_campaigns FROM Campaign")
    total_campaigns = cursor.fetchone()['total_campaigns']
    cursor.execute("SELECT COUNT(*) AS total_redeem FROM Campaign_Redemption")
    total_redeem = cursor.fetchone()['total_redeem']
    cursor.execute("""
        SELECT c.title, COUNT(r.campaign_redemption_id) AS redeem_count
        FROM Campaign c
        LEFT JOIN Campaign_Redemption r ON c.campaign_id = r.campaign_id
        GROUP BY c.campaign_id
        ORDER BY redeem_count DESC
        LIMIT 1
    """)
    top_campaign_row = cursor.fetchone()
    top_campaign = top_campaign_row['title'] if top_campaign_row else 'Không có'
    top_redeem_count = top_campaign_row['redeem_count'] if top_campaign_row else 0
    cursor.close()
    conn.close()
    return render_template(
        'campaign_service/campaign_dashboard.html',
        total_campaigns=total_campaigns,
        total_redeem=total_redeem,
        top_campaign=top_campaign,
        top_redeem_count=top_redeem_count
    )