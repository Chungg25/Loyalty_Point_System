from flask import Flask, redirect, render_template, request, jsonify, Blueprint, session
import mysql.connector
from flask_cors import CORS

transaction_bp = Blueprint("transaction", __name__)
CORS(transaction_bp)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="transaction_service"
    )

