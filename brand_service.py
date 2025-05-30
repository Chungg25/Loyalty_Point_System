from flask import Flask, render_template, request, jsonify, Blueprint
import mysql.connector
from flask_cors import CORS
from datetime import datetime

brand_bp = Blueprint("brand", __name__)
CORS(brand_bp)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database= "brand_service"
    )

# def get_db_connection():
#     return mysql.connector.connect(
#         host="han312.mysql.pythonanywhere-services.com",
#         user="han312",
#         password="SOA2025@",
#         database= "han312$brand_service"
#     )


# Existing APIs
@brand_bp.route('/get_brand', methods=['GET'])
def get_brand():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT distinct b.*, c.name, ct.* FROM Brand b
                        join Contract ct on b.brand_id = ct.brand_id
                        LEFT JOIN Category c ON b.category_id = c.category_id
                       """)
        brands = cursor.fetchall()
        cursor.close()
        conn.close()
        if not brands:
            return jsonify({"error": "No brands found"}), 404
        return jsonify({"brands": brands}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@brand_bp.route('/get_contract/<int:brand_id>', methods=['GET'])
def get_contract(brand_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Contract JOIN Brand ON Contract.brand_id = Brand.brand_id WHERE Brand.brand_id = %s", (brand_id,))
        contract = cursor.fetchall()
        cursor.close()
        conn.close()
        if not contract:
            return jsonify({"error": "No contract found"}), 404
        return jsonify({"contract": contract}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@brand_bp.route('/get_brand_id/<brand_id>', methods=['GET'])
def get_brand_by_id(brand_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Brand WHERE brand_id = %s", (brand_id,))
        brand = cursor.fetchone()
        cursor.close()
        conn.close()
        if not brand:
            return jsonify({"error": "Brand not found"}), 404
        return jsonify(brand), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@brand_bp.route('/update_brand', methods=['POST'])
def update_brand():
    data = request.get_json()
    brand_id = data.get('brand_id')
    brandname = data.get('brandname')
    email = data.get('email')
    if not brand_id or not brandname or not email:
        return jsonify({"error": "Missing required fields (brand_id, brandname, email)"}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Brand WHERE brand_id = %s", (brand_id,))
        brand = cursor.fetchone()
        if not brand:
            cursor.close()
            conn.close()
            return jsonify({"error": "Brand not found"}), 404
        cursor.execute(
            "UPDATE Brand SET brandname = %s, email = %s WHERE brand_id = %s",
            (brandname, email, brand_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "No changes made to the brand"}), 400
        cursor.close()
        conn.close()
        return jsonify({"message": "Brand updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@brand_bp.route('/update_coefficient', methods=['POST'])
def update_coefficient():
    data = request.get_json()
    brand_id = data.get('brand_id')
    coefficient = data.get('coefficient')
    if not brand_id or not coefficient:
        return jsonify({"error": "Missing required fields (brand_id, coefficient)"}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Brand WHERE brand_id = %s", (brand_id,))
        brand = cursor.fetchone()
        if not brand:
            cursor.close()
            conn.close()
            return jsonify({"error": "Brand not found"}), 404
        cursor.execute(
            "UPDATE Brand SET coefficient = %s WHERE brand_id = %s",
            (coefficient, brand_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "No changes made to the coefficient"}), 400
        cursor.close()
        conn.close()
        return jsonify({"message": "Coefficient updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# Đếm số số lượng brand
@brand_bp.route('/count_brand', methods=['GET'])
def count_brand():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as total FROM Brand")
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if not result:
            return jsonify({"error": "No brands found"}), 404
        return jsonify({"total": result['total']}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@brand_bp.route('/get_brand', methods=['GET'])
def get_all_brands():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Brand where status = 1")
        brands = cursor.fetchall()
        cursor.close()
        conn.close()

        if not brands:
            return jsonify({"error": "No brands found"}), 404
        return jsonify({"brands": brands}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@brand_bp.route('/brand_by_type_chart', methods=['GET'])
def brand_by_type_chart():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT c.name, COUNT(b.brand_id) as total FROM Brand b JOIN Category c ON b.category_id = c.category_id GROUP BY c.name")
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if not result:
            return jsonify({"error": "No brands found"}), 404
        return jsonify({"brand_by_type": result}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    
@brand_bp.route('/get_contracts', methods=['GET'])
def get_contracts():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT contract_id, brand_id, start_at, end_at, status, created_at, total_amount
            FROM Contract
            ORDER BY created_at DESC
        """)
        contracts = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"contracts": contracts}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500