from datetime import datetime
from . import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    vps = db.relationship('VPS', backref='owner', lazy=True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class VPS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contabo_id = db.Column(db.String(64), unique=True, nullable=False)
    plan = db.Column(db.String(100))
    status = db.Column(db.String(50))
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paypal_txn = db.Column(db.String(120), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
