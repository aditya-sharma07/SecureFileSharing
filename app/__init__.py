from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.ops import ops_bp
    from app.routes.client import client_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(ops_bp, url_prefix='/ops')
    app.register_blueprint(client_bp, url_prefix='/client')

    return app
