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

# Existing APIs
@brand_bp.route('/get_brand', methods=['GET'])
def get_brand():
    try: 
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT distinct b.*, c.name, ct.* FROM brand b
                        join contract ct on b.brand_id = ct.brand_id
                        LEFT JOIN Brand_Category c ON b.category_id = c.category_id
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
        cursor.execute("SELECT * FROM contract JOIN brand ON contract.brand_id = brand.brand_id WHERE brand.brand_id = %s", (brand_id,))
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
        cursor.execute("SELECT * FROM brand WHERE brand_id = %s", (brand_id,))
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
        cursor.execute("SELECT * FROM brand WHERE brand_id = %s", (brand_id,))
        brand = cursor.fetchone()
        if not brand:
            cursor.close()
            conn.close()
            return jsonify({"error": "Brand not found"}), 404
        cursor.execute(
            "UPDATE brand SET brandname = %s, email = %s WHERE brand_id = %s",
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
        cursor.execute("SELECT * FROM brand WHERE brand_id = %s", (brand_id,))
        brand = cursor.fetchone()
        if not brand:
            cursor.close()
            conn.close()
            return jsonify({"error": "Brand not found"}), 404
        cursor.execute(
            "UPDATE brand SET coefficient = %s WHERE brand_id = %s",
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
        cursor.execute("SELECT * FROM brand where status = 1")
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
        cursor.execute("SELECT c.name, COUNT(b.brand_id) as total FROM brand b JOIN Brand_Category c ON b.category_id = c.category_id GROUP BY c.name")
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if not result:
            return jsonify({"error": "No brands found"}), 404
        return jsonify({"brand_by_type": result}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# @brand_bp.route("/brand_coefficient", methods=["GET"])
# def brand_coefficient():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT brand_id, coefficient FROM brand")
#         result = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         if not result:
#             return jsonify({"error": "No brands found"}), 404
#         return jsonify({"brand_coefficient": result}), 200
#     except mysql.connector.Error as err:
#         return jsonify({"error": str(err)}), 500
