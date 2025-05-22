from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.product import Product
from app.extensions import db

product_bp = Blueprint('product', __name__)

@product_bp.route('/list', methods=['GET'])
def list_products():
    products = Product.query.filter_by(status='active').all()
    return jsonify([product.to_dict() for product in products]), 200

@product_bp.route('/add', methods=['POST'])
@jwt_required()
def add_product():
    current_user = get_jwt_identity()
    if current_user["role"] != "supplier":
        return jsonify({"msg": "Bu işlem için yetkiniz yok."}), 403

    data = request.get_json()
    if not all(key in data for key in ['name', 'price']):
        return jsonify({"msg": "Eksik bilgi. 'name' ve 'price' zorunludur."}), 400

    try:
        product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=float(data['price']),
            stock=int(data.get('stock', 0)),
            supplier_id=current_user["id"]
        )

        db.session.add(product)
        db.session.commit()

        return jsonify({"msg": "Ürün başarıyla eklendi.", "id": product.id}), 201
    except (ValueError, TypeError):
        return jsonify({"msg": "Geçersiz veri formatı. 'price' sayısal ve 'stock' tam sayı olmalıdır."}), 400

@product_bp.route('/update/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    current_user = get_jwt_identity()
    product = Product.query.get_or_404(product_id)

    if current_user["role"] != "supplier" or product.supplier_id != current_user["id"]:
        return jsonify({"msg": "Bu işlem için yetkiniz yok."}), 403

    data = request.get_json()
    try:
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = float(data['price'])
        if 'stock' in data:
            product.stock = int(data['stock'])

        db.session.commit()
        return jsonify({"msg": "Ürün başarıyla güncellendi."}), 200
    except (ValueError, TypeError):
        return jsonify({"msg": "Geçersiz veri formatı. 'price' sayısal ve 'stock' tam sayı olmalıdır."}), 400

@product_bp.route('/delete/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    current_user = get_jwt_identity()
    product = Product.query.get_or_404(product_id)

    if current_user["role"] != "supplier" or product.supplier_id != current_user["id"]:
        return jsonify({"msg": "Bu işlem için yetkiniz yok."}), 403

    product.status = 'deleted'
    db.session.commit()

    return jsonify({"msg": "Ürün başarıyla silindi."}), 200

@product_bp.route('/supplier/products', methods=['GET'])
@jwt_required()
def get_supplier_products():
    current_user = get_jwt_identity()
    if current_user["role"] != "supplier":
        return jsonify({"msg": "Bu işlem için yetkiniz yok."}), 403

    products = Product.query.filter_by(supplier_id=current_user["id"]).all()
    return jsonify([product.to_dict() for product in products]), 200 