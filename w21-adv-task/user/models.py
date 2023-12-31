from db import db

# Tabel User
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='USER')  # New field for user role
    is_suspended = db.Column(db.Boolean, default=False)
    