from app import create_app
from app.models.mongo_cart import MongoCart

# Flask uygulamasını oluştur
app = create_app()

def test_cart_operations():
    with app.app_context():
        try:
            # Test kullanıcısı için örnek ürün
            test_product = {
                "id": 1,
                "name": "Test Ürün",
                "price": 99.99,
                "quantity": 2
            }
            
            # Sepete ürün ekle
            print("Sepete ürün ekleniyor...")
            result = MongoCart.add_item(user_id=1, product_data=test_product)
            print(f"Ürün eklendi. ID: {result.inserted_id}")
            
            # Sepeti görüntüle
            print("\nSepet içeriği getiriliyor...")
            cart_items = MongoCart.get_user_cart(user_id=1)
            for item in cart_items:
                print(f"Ürün: {item['name']}, Miktar: {item['quantity']}, Fiyat: {item['price']}")
            
            # Ürün miktarını güncelle
            print("\nÜrün miktarı güncelleniyor...")
            MongoCart.update_quantity(str(result.inserted_id), quantity=3)
            print("Miktar güncellendi.")
            
            # Güncellenmiş sepeti görüntüle
            print("\nGüncellenmiş sepet içeriği:")
            cart_items = MongoCart.get_user_cart(user_id=1)
            for item in cart_items:
                print(f"Ürün: {item['name']}, Miktar: {item['quantity']}, Fiyat: {item['price']}")
            
            # Ürünü sepetten kaldır
            print("\nÜrün sepetten kaldırılıyor...")
            MongoCart.remove_item(str(result.inserted_id))
            print("Ürün kaldırıldı.")
            
            print("\nTest başarıyla tamamlandı!")
            
        except Exception as e:
            print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    test_cart_operations() 