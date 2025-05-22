import requests
import json
import sys
import traceback
import time

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
        timestamp = int(time.time())
        
        # Register test - Supplier
        supplier_email = f"supplier_{timestamp}@example.com"
        register_data = {
            "username": f"testsupplier_{timestamp}",
            "email": supplier_email,
            "password": "test123",
            "role": "supplier"
        }
        
        print("\nTesting Supplier Register:")
        register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print_response_details(register_response)

        # Register test - Customer
        customer_email = f"customer_{timestamp}@example.com"
        register_data = {
            "username": f"testcustomer_{timestamp}",
            "email": customer_email,
            "password": "test123",
            "role": "customer"
        }
        
        print("\nTesting Customer Register:")
        register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print_response_details(register_response)

        # Login test - Supplier
        login_data = {
            "email": supplier_email,
            "password": "test123"
        }
        
        print("\nTesting Supplier Login:")
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print_response_details(login_response)
        supplier_token = login_response.json().get('access_token') if login_response.status_code == 200 else None

        # Login test - Customer
        login_data = {
            "email": customer_email,
            "password": "test123"
        }
        
        print("\nTesting Customer Login:")
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print_response_details(login_response)
        customer_token = login_response.json().get('access_token') if login_response.status_code == 200 else None

        return supplier_token, customer_token
    except requests.exceptions.ConnectionError:
        print("Connection Error: Make sure Flask application is running")
        return None, None
    except Exception as e:
        print(f"Error in authentication: {str(e)}")
        traceback.print_exc()
        return None, None

def test_products(supplier_token, customer_token):
    print("\n=== Testing Product Endpoints ===")
    
    try:
        # Test with supplier token
        headers = {'Authorization': f'Bearer {supplier_token}'}

        # Get all products (empty initially)
        print("\nTesting Get All Products:")
        products_response = requests.get(f"{BASE_URL}/products/list")
        print_response_details(products_response)

        # Add a test product (as supplier)
        product_data = {
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "stock": 10
        }
        
        print("\nTesting Add Product (as supplier):")
        add_product_response = requests.post(f"{BASE_URL}/products/add", headers=headers, json=product_data)
        print_response_details(add_product_response)
        product_id = add_product_response.json().get('id') if add_product_response.status_code == 201 else None

        # Try to add product as customer (should fail)
        headers = {'Authorization': f'Bearer {customer_token}'}
        print("\nTesting Add Product (as customer - should fail):")
        add_product_response = requests.post(f"{BASE_URL}/products/add", headers=headers, json=product_data)
        print_response_details(add_product_response)

        return product_id
    except Exception as e:
        print(f"Error in products test: {str(e)}")
        traceback.print_exc()
        return None

def test_cart(customer_token, product_id):
    print("\n=== Testing Cart Endpoints ===")
    headers = {'Authorization': f'Bearer {customer_token}'}

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
        get_cart_response = requests.get(f"{BASE_URL}/cart/items", headers=headers)
        print_response_details(get_cart_response)

        # Update cart item quantity
        if get_cart_response.status_code == 200:
            cart_items = get_cart_response.json()
            if cart_items:
                item_id = cart_items[0].get('_id')
                print("\nTesting Update Cart Item Quantity:")
                update_response = requests.put(
                    f"{BASE_URL}/cart/update/{item_id}",
                    headers=headers,
                    json={"quantity": 3}
                )
                print_response_details(update_response)

                # Remove item from cart
                print("\nTesting Remove Cart Item:")
                remove_response = requests.delete(f"{BASE_URL}/cart/remove/{item_id}", headers=headers)
                print_response_details(remove_response)

    except Exception as e:
        print(f"Error in cart test: {str(e)}")
        traceback.print_exc()

def test_user_profile(supplier_token, customer_token):
    print("\n=== Testing User Profile Endpoints ===")
    
    try:
        # Test supplier profile
        headers = {'Authorization': f'Bearer {supplier_token}'}
        print("\nTesting Get Supplier Profile:")
        profile_response = requests.get(f"{BASE_URL}/user/profile", headers=headers)
        print_response_details(profile_response)

        # Update supplier profile
        update_data = {
            "first_name": "Updated Supplier",
            "last_name": "Test"
        }
        print("\nTesting Update Supplier Profile:")
        update_response = requests.put(f"{BASE_URL}/user/profile", headers=headers, json=update_data)
        print_response_details(update_response)

        # Test customer profile
        headers = {'Authorization': f'Bearer {customer_token}'}
        print("\nTesting Get Customer Profile:")
        profile_response = requests.get(f"{BASE_URL}/user/profile", headers=headers)
        print_response_details(profile_response)

    except Exception as e:
        print(f"Error in profile test: {str(e)}")
        traceback.print_exc()

def run_all_tests():
    try:
        print("Starting API Tests...")
        print(f"Testing against server: {BASE_URL}")
        
        # Wait for Flask to start
        time.sleep(2)
        
        # Test server availability
        try:
            requests.get(BASE_URL)
        except requests.exceptions.ConnectionError:
            print("Error: Cannot connect to the server. Make sure Flask application is running.")
            return

        # Run authentication tests and get tokens
        supplier_token, customer_token = test_auth()
        if supplier_token and customer_token:
            # Run product tests
            product_id = test_products(supplier_token, customer_token)
            if product_id:
                # Run cart tests with customer token
                test_cart(customer_token, product_id)
            # Run user profile tests
            test_user_profile(supplier_token, customer_token)
        else:
            print("Authentication failed, skipping remaining tests")
    except Exception as e:
        print(f"\nError occurred during testing: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests() 