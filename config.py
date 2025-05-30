import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "./uploads")

    # Email
    MAIL_SERVER = os.getenv("EMAIL_HOST")
    MAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.getenv("EMAIL_HOST_USER")
    MAIL_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("EMAIL_SENDER")

    # Security salts
    DOWNLOAD_URL_SALT = os.getenv("DOWNLOAD_URL_SALT")
    DOWNLOAD_URL_EXPIRATION = int(os.getenv("DOWNLOAD_URL_EXPIRATION", 3600))
    VERIFICATION_URL_SALT = os.getenv("VERIFICATION_URL_SALT")
    VERIFICATION_URL_EXPIRATION = int(os.getenv("VERIFICATION_URL_EXPIRATION", 86400))
