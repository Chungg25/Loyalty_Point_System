from flask import request, jsonify, Blueprint, render_template, redirect, session
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

@point_bp.route('/get_total_points/<int:brand_id>', methods=['GET'])
def get_total_points(brand_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT SUM(pl.points) AS total_points
            FROM point_log pl
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

@point_bp.route('/get_points/<int:user_id>', methods=['GET'])
def get_points(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT total_points from pointwallet where user_id = %s
        """, (user_id,))
        points = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(points), 200

    except mysql.connector.Error as err:
        print(f"Error fetching points: {err}")
        return jsonify({"error": str(err)}), 500
    
@point_bp.route('/get_payments/<int:brand_id>', methods=['GET'])
def get_payments(brand_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.transaction_id, t.invoice_code AS transaction_id, 
                   us.fullname AS customer_name, 
                   DATE_FORMAT(t.created_at, '%d/%m/%Y') AS payment_date, 
                   t.amount, 
                   FLOOR(
                       t.amount / cr.rate * mtc.member_coefficient * b.coefficient
                   ) AS points_earned,
                   'Hoàn thành' AS status
            FROM Transactions t
            JOIN user_snapshot us ON t.user_snapshot_id = us.user_snapshot_id
            JOIN Brand_Service.Brand b ON t.brand_id = b.brand_id
            JOIN User_Service.Customer c ON t.user_id = c.user_id
            JOIN User_Service.MemberTypeCoefficient mtc ON c.membertype = mtc.membertype
            JOIN ConversionRule cr 
                ON t.created_at BETWEEN cr.effective_from AND IFNULL(cr.effective_to, NOW())
            WHERE t.brand_id = %s
            LIMIT 4
        """, (brand_id,))
        payments = cursor.fetchall()
        cursor.close()
        conn.close()
        if not payments:
            return jsonify({"error": "No payments found"}), 404
        return jsonify({"payments": payments}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    
@point_bp.route('/monthly_revenue', methods=['GET'])
def monthly_vevenue():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT  SUM(t.amount) AS total
            FROM Transactions t
            GROUP BY MONTH(t.created_at)
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