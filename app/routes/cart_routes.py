from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.mongo_cart import MongoCart
from app.models.product import Product
from app.utils.mailer import send_cart_update_email

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    current_user = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    product = Product.query.get_or_404(product_id)
    if product.status != 'active':
        return jsonify({"msg": "Bu ürün artık mevcut değil."}), 400

    product_data = {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "quantity": quantity
    }

    MongoCart.add_item(current_user["id"], product_data)
    send_cart_update_email(current_user["email"], "Sepetiniz Güncellendi", "Sepetinize yeni bir ürün eklendi.")
    
    return jsonify({"msg": "Ürün sepete eklendi."}), 201

@cart_bp.route('/items', methods=['GET'])
@jwt_required()
def get_cart_items():
    current_user = get_jwt_identity()
    cart_items = MongoCart.get_user_cart(current_user["id"])
    return jsonify(cart_items), 200

@cart_bp.route('/update/<item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    data = request.get_json()
    quantity = data.get('quantity')
    
    if not quantity or quantity < 1:
        return jsonify({"msg": "Geçersiz miktar."}), 400

    MongoCart.update_quantity(item_id, quantity)
    return jsonify({"msg": "Sepet güncellendi."}), 200

@cart_bp.route('/remove/<item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    MongoCart.remove_item(item_id)
    return jsonify({"msg": "Ürün sepetten kaldırıldı."}), 200