from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import mongo 



cart_bp = Blueprint('cart_bp', __name__)

# Sepete ürün ekleme
@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    data = request.get_json()
    user_id = get_jwt_identity()

    new_cart_item = {
        "user_id": user_id,
        "product_id": data["product_id"],
        "product_name": data["product_name"],
        "price": data["price"],
        "quantity": data["quantity"],
        "status": "active"
    }


    mongo.db.cart.insert_one(new_cart_item)
    return jsonify({"message": "Ürün sepete eklendi!"}), 201

# Sepeti görüntüleme
@cart_bp.route('/my-cart', methods=['GET'])
@jwt_required()
def get_my_cart():
       identity = get_jwt_identity()
       user_id = identity['id']

       cart_items = list(mongo.db.cart.find({"user_id": user_id}, {'_id': 0}))

       return jsonify(cart_items), 200



# Sepetten ürün silme
@cart_bp.route('/remove/<product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(product_id):
    identity = get_jwt_identity()
    user_id = identity['id']

    result = mongo.db.cart.delete_one({"user_id": user_id, "product_id": product_id})
    if result.deleted_count == 0:
        return jsonify({"msg": "Ürün bulunamadı."}), 404

    return jsonify({"msg": "Ürün sepetten silindi!"}), 200