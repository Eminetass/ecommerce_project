# 📦 Ecommerce API Projesi

Bu proje Flask tabanlı bir e-ticaret API uygulamasıdır.  
✅ MySQL ve MongoDB veri tabanlarıyla çalışır.  
✅ JWT authentication kullanır.  
✅ Mail bildirim sistemi mevcuttur.

---

## 📌 Kurulum Adımları

### 1️⃣ Projeyi Klonla
```bash
git clone <repo-linki>
cd ecommerce_project


2️⃣ Sanal Ortam Oluştur ve Aktifleştir
conda create -n virtualEnv python=3.11
conda activate virtualEnv

3️⃣ Gerekli Kütüphaneleri Yükle
pip install -r requirements.txt

4️⃣ MySQL ve MongoDB Ayarlarını Yap
MySQL'de veritabanını ve kullanıcıyı oluştur:
CREATE DATABASE ecommerce_db;
CREATE USER 'ecom_user'@'localhost' IDENTIFIED BY 'EmnTs123.';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecom_user'@'localhost';
FLUSH PRIVILEGES;
MongoDB servisinin çalıştığından emin ol:
mongod
Not: Eğer mongod komutu bulunamıyor hatası alırsan MongoDB bin dizinini PATH'e eklemen gerekebilir.

📌 .env Dosyası
Proje ana dizinine .env dosyası oluşturup aşağıdaki bilgileri ekleyin:

# MySQL Ayarları
MYSQL_USER=ecom_user
MYSQL_PASSWORD=EmnTs123.
MYSQL_HOST=localhost
MYSQL_DATABASE=ecommerce_db

# MongoDB Ayarları
MONGO_URI=mongodb://localhost:27017/ecommerce_cart

# JWT Ayarı
JWT_SECRET_KEY=supersecretjwtkey

# Mail Ayarları (Örn: Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=youremail@gmail.com
MAIL_PASSWORD=yourapppassword


📌 Uygulamayı Çalıştırma
python run.py



📌 API Endpointleri
📝 Auth
POST /auth/register → Üye ol

POST /auth/login → Giriş yap

POST /auth/reset-password-request → Şifre sıfırlama isteği

POST /auth/reset-password/<token> → Şifre sıfırla

👤 User
PUT /user/update → Profil güncelle

📦 Product
POST /products/add → Ürün ekle (supplier)

PUT /products/update/<id> → Ürün güncelle (supplier)

DELETE /products/delete/<id> → Ürün sil (supplier)

🛒 Cart
POST /cart/add → Sepete ürün ekle

GET /cart/my-cart → Sepeti görüntüle

DELETE /cart/remove/<product_id> → Sepetten ürün sil




📌 Notlar
Postman ile JWT token'ı Authorization: Bearer <token> olarak header'a ekleyin.

Ürün ekleme, güncelleme ve silme işlemleri sadece supplier kullanıcı rolüne sahip hesaplarca yapılabilir.


✨ Katkıda Bulunmak
Fork'la → branch aç → geliştirmeni yap → pull request at 🎉
