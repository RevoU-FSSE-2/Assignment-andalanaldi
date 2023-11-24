from flask import Blueprint, request
from following.models import Following
from user.models import User
from auth.utils import decode_jwt
from db import db

following_blueprint = Blueprint("following", __name__)

@following_blueprint.route("/", methods=["POST"])
def follow_unfollow_user():
    data = request.get_json()
    token = request.headers.get('Authorization')
    if not token:
        return {"error": "Token is missing"}, 401

    payload = decode_jwt(token)
    if not payload:
        return {"error": "Token is not valid!"}, 401

    user_id = payload.get("user_id")
    user_to_follow_id = data.get("user_id")

    if not user_to_follow_id:
        return {"error": "User ID to follow/unfollow is missing"}, 400

    if user_id == user_to_follow_id:
        return {"error": "Cannot follow/unfollow yourself"}, 400

    follower = User.query.get(user_id)
    user_to_follow = User.query.get(user_to_follow_id)

    if not follower or not user_to_follow:
        return {"error": "User(s) not found"}, 404

    existing_follow = Following.query.filter_by(follower_id=user_id, followed_user_id=user_to_follow_id).first()

    if existing_follow:
        db.session.delete(existing_follow)
        db.session.commit()
        return {"following_status": "unfollow"}, 200
    else:
        new_follow = Following(follower_id=user_id, followed_user_id=user_to_follow_id)
        db.session.add(new_follow)
        db.session.commit()
        return {"following_status": "follow"}, 200
