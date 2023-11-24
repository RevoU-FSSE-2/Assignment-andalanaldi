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
    # email = fields.Email(required=True)

@auth_blp.route("/registration", methods=["POST"])
def register():
    data = request.get_json()
    schema = UserRegistrationSchema()
    # username = data["username"] # not needed to hardcode anymore if schemas exist
    # password = data["password"]
    # email = data["email"]
    try:
        data = schema.load(data)
    except ValidationError as err:
        return {"error": err.messages}, 400
    # has not been validated yet, need schemas
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    # None
    new_user = User(username=data['username'], bio=data['bio'], password=hashed_password)
    # new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return {
        'user_id': new_user.user_id,
        'username': new_user.username,
        'bio': new_user.bio
    }

@auth_blp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data["username"]
    password = data["password"]
    # filter di sql alchemy ga bisa langsung return username, username unique, use first()
    # user 1 object, user or password is not valid ?
    if not username or not password:
        return ({"error": "Username or password is missing"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return {"error": "Username or password is not valid"}, 401
    
    valid_password = bcrypt.check_password_hash(user.password, password)
    if not valid_password:
        return {"error": "Username or password is not valid"}, 401
    
    payload = {
        'user_id': user.user_id,
        'username': user.username,
        # 'bio': user.bio,
        # 'email': user.email,
        'exp': datetime.utcnow() + timedelta(minutes=30) # extend token expiration from 1 to 30 minutes to help debugging
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm="HS256")
    
    return {
        # 'user_id': user.user_id,
        # 'username': user.username,
        'token': token
    }
 
    # }
    # token auth needed if we not only have just 
    # public api for login regis but we need token 
    # for user to access their profile for instance
 

