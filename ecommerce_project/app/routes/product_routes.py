from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.product import Product

product_bp = Blueprint('product', __name__)

# Ürün ekleme
@product_bp.route('/add', methods=['POST'])
@jwt_required()
def add_product():
    identity = get_jwt_identity()
    if identity["role"] != "supplier":
        return jsonify({"msg": "Sadece tedarikçiler ürün ekleyebilir."}), 403

    data = request.get_json()

    required_fields = ["name", "price", "stock"]
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Eksik veri var. name, price, stock zorunlu."}), 400

    product = Product(
        name=data["name"],
        description=data.get("description", ""),
        price=data["price"],
        stock=data["stock"],
        supplier_id=identity["id"]
    )
    db.session.add(product)
    db.session.commit()

    return jsonify({"msg": "Ürün başarıyla eklendi."}), 201


# Ürün güncelleme
@product_bp.route('/update/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    identity = get_jwt_identity()
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"msg": "Ürün bulunamadı."}), 404

    if product.supplier_id != identity["id"]:
        return jsonify({"msg": "Bu ürünü sadece sahibi güncelleyebilir."}), 403

    data = request.get_json()

    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)

    db.session.commit()

    return jsonify({"msg": "Ürün başarıyla güncellendi."}), 200


# Ürün silme
@product_bp.route('/delete/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    identity = get_jwt_identity()
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"msg": "Ürün bulunamadı."}), 404

    if product.supplier_id != identity["id"]:
        return jsonify({"msg": "Bu ürünü sadece sahibi silebilir."}), 403

    product.status = "deleted"  # Değişiklik burada!
    db.session.commit()

    return jsonify({"msg": "Ürün başarıyla silindi (soft delete yapıldı)."}), 200



# Ürün listeleme (public)
@product_bp.route('/', methods=['GET'])
def list_products():
    products = Product.query.filter_by(status="active").all()
    result = []
    for product in products:
        result.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "supplier_id": product.supplier_id
        })
    return jsonify(result), 200

