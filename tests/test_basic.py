def test_app_is_created(app):
    assert app is not None
    assert app.config['TESTING'] is True

def test_home_page(client):
    response = client.get('/')
    assert response.status_code in (200, 302)  # Either OK or redirect

def test_products_page(client):
    response = client.get('/products')
    assert response.status_code in (200, 302)

def test_login_page(client):
    response = client.get('/auth/login')
    assert response.status_code in (200, 302) 