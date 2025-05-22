import pytest
from app.models.mongo_cart import MongoCart
from app.extensions import mongo

def test_mongo_cart_creation():
    cart = MongoCart()
    assert cart is not None

def test_add_item_to_cart():
    cart = MongoCart()
    product_data = {
        'product_id': '1',
        'name': 'Test Product',
        'quantity': 2,
        'price': 10.99
    }
    result = cart.add_item(product_data=product_data)
    assert result is True

def test_get_cart_items():
    cart = MongoCart()
    items = cart.get_user_cart(user_id=1)
    assert isinstance(items, list)

def test_update_cart_item():
    cart = MongoCart()
    product_data = {
        'product_id': '1',
        'name': 'Test Product',
        'quantity': 3,
        'price': 10.99
    }
    cart.add_item(product_data=product_data)
    update_result = cart.update_quantity(item_id='1', quantity=4)
    assert update_result is True

def test_remove_cart_item():
    cart = MongoCart()
    product_data = {
        'product_id': '1',
        'name': 'Test Product',
        'quantity': 2,
        'price': 10.99
    }
    cart.add_item(product_data=product_data)
    remove_result = cart.remove_item(item_id='1')
    assert remove_result is True 