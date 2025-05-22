import pytest
from app.models.product import Product
from app.extensions import db

def test_create_product(init_database):
    product = Product(
        name='Test Product',
        description='Test Description',
        price=99.99,
        stock=10
    )
    db.session.add(product)
    db.session.commit()
    
    assert product.id is not None
    assert product.name == 'Test Product'

def test_get_product(init_database):
    product = Product(
        name='Test Product',
        description='Test Description',
        price=99.99,
        stock=10
    )
    db.session.add(product)
    db.session.commit()
    
    retrieved_product = Product.query.filter_by(name='Test Product').first()
    assert retrieved_product is not None
    assert retrieved_product.price == 99.99

def test_update_product(init_database):
    product = Product(
        name='Test Product',
        description='Test Description',
        price=99.99,
        stock=10
    )
    db.session.add(product)
    db.session.commit()
    
    product.price = 89.99
    db.session.commit()
    
    updated_product = Product.query.filter_by(name='Test Product').first()
    assert updated_product.price == 89.99

def test_delete_product(init_database):
    product = Product(
        name='Test Product',
        description='Test Description',
        price=99.99,
        stock=10
    )
    db.session.add(product)
    db.session.commit()
    
    db.session.delete(product)
    db.session.commit()
    
    deleted_product = Product.query.filter_by(name='Test Product').first()
    assert deleted_product is None 