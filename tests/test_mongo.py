from pymongo import MongoClient
from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

# MongoDB bağlantı URI'sini al
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/ecommerce")

try:
    # MongoDB'ye bağlan
    client = MongoClient(MONGO_URI)
    
    # Veritabanını seç
    db = client.ecommerce
    
    # Bağlantıyı test et
    client.server_info()
    
    print("MongoDB bağlantısı başarılı!")
    print(f"Veritabanları: {client.list_database_names()}")
    
    # Test koleksiyonu oluştur
    test_collection = db.test_collection
    
    # Test verisi ekle
    test_data = {"message": "Test başarılı!"}
    result = test_collection.insert_one(test_data)
    
    print(f"Test verisi eklendi. ID: {result.inserted_id}")
    
    # Test verisini sil
    test_collection.delete_one({"_id": result.inserted_id})
    
except Exception as e:
    print(f"Hata: {e}")
finally:
    if 'client' in locals():
        client.close()
        print("MongoDB bağlantısı kapatıldı.") 