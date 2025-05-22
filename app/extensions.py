from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_mail import Mail

db = SQLAlchemy()
mongo = PyMongo()
jwt = JWTManager()
mail = Mail() 