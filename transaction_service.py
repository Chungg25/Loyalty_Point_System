from flask import Flask, render_template, request, jsonify, Blueprint, render_template
import mysql.connector
from flask_cors import CORS

user_bp = Blueprint("transaction", __name__)
CORS(user_bp)