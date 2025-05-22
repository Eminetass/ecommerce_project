import requests
import json
import sys
import traceback

BASE_URL = "http://localhost:5000"

def print_response_details(response):
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    try:
        print(f"Response Body: {response.json()}")
    except:
        print(f"Response Text: {response.text}")

def test_auth():
    print("\n=== Testing Authentication Endpoints ===")
    
    try:
        # Register test
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "test123",
            "role": "customer"
        }
        
        print("\nTesting Register:")
        register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print_response_details(register_response)

        # Login test
        login_data = {
            "email": "test@example.com",
            "password": "test123"
        }
        
        print("\nTesting Login:")
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print_response_details(login_response)
        
        if login_response.status_code == 200:
            return login_response.json().get('access_token')
        else:
            print("Failed to get access token")
            return None
    except requests.exceptions.ConnectionError:
        print("Connection Error: Make sure Flask application is running")
        return None
    except Exception as e:
        print(f"Error in authentication: {str(e)}")
        traceback.print_exc()
        return None

def test_products(token):
    print("\n=== Testing Product Endpoints ===")
    headers = {'Authorization': f'Bearer {token}'}

    try:
        # Get all products
        print("\nTesting Get All Products:")
        products_response = requests.get(f"{BASE_URL}/products", headers=headers)
        print_response_details(products_response)

        # Add a test product
        product_data = {
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "stock": 10
        }
        
        print("\nTesting Add Product:")
        add_product_response = requests.post(f"{BASE_URL}/products", headers=headers, json=product_data)
        print_response_details(add_product_response)
        
        if add_product_response.status_code == 201:
            return add_product_response.json().get('id')
        return None
    except Exception as e:
        print(f"Error in products test: {str(e)}")
        traceback.print_exc()
        return None

def test_cart(token, product_id):
    print("\n=== Testing Cart Endpoints ===")
    headers = {'Authorization': f'Bearer {token}'}

    try:
        # Add item to cart
        cart_data = {
            "product_id": product_id,
            "quantity": 2
        }
        
        print("\nTesting Add to Cart:")
        add_cart_response = requests.post(f"{BASE_URL}/cart/add", headers=headers, json=cart_data)
        print_response_details(add_cart_response)

        # Get cart
        print("\nTesting Get Cart:")
        get_cart_response = requests.get(f"{BASE_URL}/cart", headers=headers)
        print_response_details(get_cart_response)
    except Exception as e:
        print(f"Error in cart test: {str(e)}")
        traceback.print_exc()

def test_user_profile(token):
    print("\n=== Testing User Profile Endpoints ===")
    headers = {'Authorization': f'Bearer {token}'}

    try:
        # Get user profile
        print("\nTesting Get Profile:")
        profile_response = requests.get(f"{BASE_URL}/user/profile", headers=headers)
        print_response_details(profile_response)
    except Exception as e:
        print(f"Error in profile test: {str(e)}")
        traceback.print_exc()

def run_all_tests():
    try:
        print("Starting API Tests...")
        print(f"Testing against server: {BASE_URL}")
        
        # Test server availability
        try:
            requests.get(BASE_URL)
        except requests.exceptions.ConnectionError:
            print("Error: Cannot connect to the server. Make sure Flask application is running.")
            return

        # Run authentication tests and get token
        token = test_auth()
        if token:
            # Run product tests
            product_id = test_products(token)
            if product_id:
                # Run cart tests
                test_cart(token, product_id)
            # Run user profile tests
            test_user_profile(token)
        else:
            print("Authentication failed, skipping remaining tests")
    except Exception as e:
        print(f"\nError occurred during testing: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests() 