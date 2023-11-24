from db import db
from datetime import datetime

# Tabel User
class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False) # ForeignKey should match the actual column name in the User table
    published_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tweet = db.Column(db.String(150), nullable=False)   