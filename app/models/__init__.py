from app.extensions import db

__all__ = ['db']

# Import models after db is defined
from .user import User
from .product import Product
from .cart import Cart

__all__ += ['User', 'Product', 'Cart'] 