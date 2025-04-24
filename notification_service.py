from flask import Flask, render_template, request, jsonify, Blueprint, render_template
import mysql.connector
from datetime import datetime
from flask_cors import CORS

notification_bp = Blueprint("notification", __name__)
CORS(notification_bp)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="notification_service"
    )

# 1. Trang chủ thông báo
@notification_bp.route('/notification', methods=['GET'])
def notification():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Notification WHERE status = 1")
        notifications = cursor.fetchall()
        return render_template('notification_service/notification.html', notifications=notifications)
    except Exception as e:
        return render_template('notification_service/error.html', message=str(e)), 500
    finally:
        cursor.close()
        conn.close()

# 2. Tạo thông báo
@notification_bp.route('/create_notification_form', methods=['GET'])
def create_notification_form():
    return render_template('/notification_service/create_notification.html')

@notification_bp.route('/create_notification', methods=['POST'])
def create_notification():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data received'}), 400

    try:
        title = data.get('title')
        message = data.get('message')

        created_at_str = data.get('created_at')
        end_at_str = data.get('end_at')

        # Chuyển đổi định dạng thời gian
        created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M") if created_at_str else None
        end_at = datetime.strptime(end_at_str, "%Y-%m-%dT%H:%M") if end_at_str else None
        
        status = int(data.get('status'))

        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO Notification (title, message, created_at, end_at, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (title, message, created_at, end_at, status))
            connection.commit()

        return jsonify({'message': 'Tạo thông báo thành công'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        connection.close()

# 3. Cập nhật thông báo
@notification_bp.route('/update_notification/<int:notification_id>', methods=['PUT'])
def update_notification(notification_id):
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            UPDATE Notification
            SET title = %s, message = %s, end_at = %s
            WHERE notification_id = %s
        """
        cursor.execute(query, (
            data['title'],
            data['message'],
            data.get('end_at'),
            notification_id
        ))
        conn.commit()

        return jsonify({'message': 'Notification updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 4. Xóa thông báo
@notification_bp.route('/delete_notification/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Notification WHERE notification_id = %s", (notification_id,))
        conn.commit()

        return jsonify({'message': 'Notification deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 5. Tắt/mở thông báo
@notification_bp.route('/toggle_notification_status/<int:notification_id>/toggle', methods=['PATCH'])
def toggle_notification_status(notification_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            UPDATE Notification
            SET status = CASE
               WHEN status = 1 THEN 0
               WHEN status = 0 THEN 1
            END
            WHERE notification_id = %s
            RETURNING status""", (notification_id,))
        conn.commit()

        return jsonify({'message': 'Notification status updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
