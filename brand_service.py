from flask import Flask, render_template, request, jsonify, Blueprint, render_template
import mysql.connector
from flask_cors import CORS

brand_bp = Blueprint("brand", __name__)
CORS(brand_bp)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="brand_service"
    )

@brand_bp.route('/get_brand', methods=['GET'])
def get_brand():
    try: 
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Brand")
        brands = cursor.fetchall()
        cursor.close()
        conn.close()

        if not brands:
            return jsonify({"error": "No brands found"}), 404
        return jsonify(brands), 200
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
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        # Check if the brand exists
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Brand WHERE brand_id = %s", (brand_id,))
        brand = cursor.fetchone()

        if not brand:
            cursor.close()
            conn.close()
            return jsonify({"error": "Brand not found"}), 404

        # Update the brand
        cursor.execute(
            "UPDATE Brand SET brandname = %s, email = %s WHERE brand_id = %s",
            (brandname, email, brand_id)
        )
        conn.commit()

        # Check if any rows were affected
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
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        # Check if the brand exists
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Brand WHERE brand_id = %s", (brand_id,))
        brand = cursor.fetchone()

        if not brand:
            cursor.close()
            conn.close()
            return jsonify({"error": "Brand not found"}), 404

        # Update the coefficient
        cursor.execute(
            "UPDATE Brand SET coefficient = %s WHERE brand_id = %s",
            (coefficient, brand_id)
        )
        conn.commit()

        # Check if any rows were affected
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "No changes made to the coefficient"}), 400

        cursor.close()
        conn.close()
        return jsonify({"message": "Coefficient updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500