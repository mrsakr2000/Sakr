from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from .config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    with app.app_context():
        db.create_all()

    from .routes.auth import auth_bp
    from .routes.vps import vps_bp
    from .routes.payments import payments_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(vps_bp, url_prefix='/vps')
    app.register_blueprint(payments_bp, url_prefix='/payments')

    return app
