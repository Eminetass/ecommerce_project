from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from app.config import Config
from app.models import db  # sadece bu olacak
from app.routes.cart_routes import cart_bp
from app.extensions import db, mongo, jwt, mail  # 🔥 burada çağırdık
from app.routes.product_routes import product_bp
from app.routes.user_routes import user_bp



mongo = PyMongo()
jwt = JWTManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    mongo.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.product_routes import product_bp
    from app.routes.cart_routes import cart_bp
    from app.routes.user_routes import user_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(product_bp, url_prefix="/products")
    app.register_blueprint(cart_bp, url_prefix="/cart")
    app.register_blueprint(user_bp, url_prefix="/user")


    # Tabloları oluştur
    with app.app_context():
        from app.models import user, product, cart  # modeller import edilmeli ki create_all çalışsın
        db.create_all()

    return app
