from flask import Blueprint, request, jsonify, current_app
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .database import get_db
from .utils import sanitize_input

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = sanitize_input(data.get('username'))
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    db = get_db()
    
    # Параметризованный запрос
    user = db.execute(
        "SELECT id FROM users WHERE username = ?", 
        (username,)
    ).fetchone()

    if user:
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = generate_password_hash(password, method='scrypt')
    
    # Параметризованный запрос
    db.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password)
    )
    db.commit()

    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = sanitize_input(data.get('username'))
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    db = get_db()
    
    # Параметризованный запрос
    user = db.execute(
        "SELECT * FROM users WHERE username = ?", 
        (username,)
    ).fetchone()

    if not user or not check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        'user_id': user['id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

    return jsonify({"token": token}), 200
