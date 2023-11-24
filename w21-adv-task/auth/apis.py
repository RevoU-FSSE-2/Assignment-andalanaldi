from flask import Blueprint, request
from common.bcrypt import bcrypt
from user.models import User
from db import db
import jwt, os
from datetime import datetime, timedelta
from marshmallow import Schema, fields, ValidationError

auth_blp = Blueprint("auth", __name__)

class UserRegistrationSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    bio = fields.String(required=True)
    role = fields.String(required=True)  # Include role in the schema

@auth_blp.route("/registration", methods=["POST"])
def register():
    data = request.get_json()
    schema = UserRegistrationSchema()

    try:
        data = schema.load(data)
    except ValidationError as err:
        return {"error": err.messages}, 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    new_user = User(
        username=data['username'], 
        bio=data['bio'], 
        password=hashed_password,
        role=data['role'] # Set the role for the new user
    )
    
    db.session.add(new_user)
    db.session.commit()

    return {
        'user_id': new_user.user_id,
        'username': new_user.username,
        'bio': new_user.bio,
        'role': new_user.role  # Return the role in the response        
    }

@auth_blp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data["username"]
    password = data["password"]

    if not username or not password:
        return ({"error": "Username or password is missing"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return {"error": "Username or password is not valid"}, 401

    if user.is_suspended:
        return {"error": "Account is suspended"}, 401

    valid_password = bcrypt.check_password_hash(user.password, password)
    if not valid_password:
        return {"error": "Username or password is not valid"}, 401
    
    payload = {
        'user_id': user.user_id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(minutes=30) # extend token expiration from 1 to 30 minutes to help debugging
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm="HS256")
    
    return {
        'token': token
    }
 

