from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.product import Product
from app.extensions import db

product_bp = Blueprint('product', __name__)

# Ürün ekleme
@product_bp.route('/add', methods=['POST'])
@jwt_required()
def add_product():
    current_user = get_jwt_identity()
    if current_user["role"] != "supplier":
        return jsonify({"msg": "Bu işlem için yetkiniz yok."}), 403

    data = request.get_json()
    product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        stock=data.get('stock', 0),
        supplier_id=current_user["id"]
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({"msg": "Ürün başarıyla eklendi.", "id": product.id}), 201


# Ürün güncelleme
@product_bp.route('/update/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    current_user = get_jwt_identity()
    product = Product.query.get_or_404(product_id)

    if current_user["role"] != "supplier" or product.supplier_id != current_user["id"]:
        return jsonify({"msg": "Bu işlem için yetkiniz yok."}), 403

    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)

    db.session.commit()
    return jsonify({"msg": "Ürün başarıyla güncellendi."}), 200


# Ürün silme
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


# Ürün listeleme (public)
@product_bp.route('/list', methods=['GET'])
def list_products():
    products = Product.query.filter_by(status='active').all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'stock': p.stock,
        'supplier_id': p.supplier_id
    } for p in products]), 200


@product_bp.route('/supplier/products', methods=['GET'])
@jwt_required()
def get_supplier_products():
    current_user = get_jwt_identity()
    if current_user["role"] != "supplier":
        return jsonify({"msg": "Bu işlem için yetkiniz yok."}), 403

    products = Product.query.filter_by(supplier_id=current_user["id"]).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'stock': p.stock,
        'status': p.status
    } for p in products]), 200


@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.status != 'active':
        return jsonify({"msg": "Bu ürün artık mevcut değil."}), 404

    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'supplier_id': product.supplier_id
    }), 200
