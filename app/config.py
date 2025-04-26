import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MySQL
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI")

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
