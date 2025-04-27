from flask import Blueprint

product_bp = Blueprint('product', __name__)

# Şimdilik boş kalsın, sadece Blueprint tanımı olsun.
@product_bp.route('/')
def index():
    return "Product route çalışıyor!"
