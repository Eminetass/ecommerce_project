from flask import Flask
from app.config import Config
from app.extensions import db, mongo, jwt, mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    mongo.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    with app.app_context():
        # Import models
        from app.models.user import User
        from app.models.product import Product
        from app.models.cart import Cart

        # Import routes
        from app.routes.auth_routes import auth_bp
        from app.routes.product_routes import product_bp
        from app.routes.cart_routes import cart_bp
        from app.routes.user_routes import user_bp

        # Register blueprints
        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(product_bp, url_prefix="/products")
        app.register_blueprint(cart_bp, url_prefix="/cart")
        app.register_blueprint(user_bp, url_prefix="/user")

        # Create tables
        db.create_all()

    return app 