from flask import Blueprint

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/')
def index():
    return "Cart route çalışıyor!"
