import pytest
from app.models.user import User
from app.extensions import db
import json

def test_register(client, init_database):
    response = client.post('/auth/register', json={
        'email': 'test@test.com',
        'password': 'test123',
        'name': 'Test User'
    })
    assert response.status_code in (200, 201)
    
    user = User.query.filter_by(email='test@test.com').first()
    assert user is not None
    assert user.name == 'Test User'

def test_login(client, init_database):
    # First register a user
    client.post('/auth/register', json={
        'email': 'test@test.com',
        'password': 'test123',
        'name': 'Test User'
    })
    
    # Then try to login
    response = client.post('/auth/login', json={
        'email': 'test@test.com',
        'password': 'test123'
    })
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'access_token' in data

def test_invalid_login(client, init_database):
    response = client.post('/auth/login', json={
        'email': 'wrong@test.com',
        'password': 'wrongpass'
    })
    assert response.status_code == 401

def test_protected_route(client, init_database):
    # First register and login
    client.post('/auth/register', json={
        'email': 'test@test.com',
        'password': 'test123',
        'name': 'Test User'
    })
    
    login_response = client.post('/auth/login', json={
        'email': 'test@test.com',
        'password': 'test123'
    })
    
    token = json.loads(login_response.data)['access_token']
    
    # Try accessing a protected route
    response = client.get('/user/profile', 
                         headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200 