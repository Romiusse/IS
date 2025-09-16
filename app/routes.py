from flask import Blueprint, request, jsonify
from .database import get_db
from .middlewares import jwt_required
from .utils import sanitize_input

api_bp = Blueprint('api', __name__)

@api_bp.route('/items', methods=['GET'])
@jwt_required
def get_items():
    db = get_db()
    
    # Параметризованный запрос
    items = db.execute(
        "SELECT content FROM items WHERE user_id = ?",
        (request.user_id,)
    ).fetchall()
    
    return jsonify([item['content'] for item in items]), 200

@api_bp.route('/items', methods=['POST'])
@jwt_required
def add_item():
    item_content = sanitize_input(request.json.get('item'))
    
    if not item_content:
        return jsonify({"error": "Item content is required"}), 400

    db = get_db()
    
    # Параметризованный запрос
    db.execute(
        "INSERT INTO items (content, user_id) VALUES (?, ?)",
        (item_content, request.user_id)
    )
    db.commit()
    
    return jsonify({"message": "Item added successfully"}), 201
