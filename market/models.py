from market import db, login_manager
from market import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(user_id=user_id).first()

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(25), nullable=False, unique=True)
    password_hash = db.Column(db.String(64), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)

    items_owned = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
           return (self.user_id)
        

class Item(db.Model):
    item_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(8), nullable=False)
    info = db.Column(db.String(1024), nullable=False)

    owner = db.Column(db.Integer(), db.ForeignKey('user.user_id'))

    def __repr__(self):
        return f"item_id: {self.item_id} | name: {self.name}"