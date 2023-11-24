from flask import Blueprint, request
from user.models import User
from tweet.models import Tweet
from following.models import Following
from auth.utils import decode_jwt
from db import db

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route("/", methods=["GET"])
def get_user_profile():
    token = request.headers.get('Authorization')
    if not token:
        return {"error": "Token is missing"}, 401

    payload = decode_jwt(token)
    if not payload:
        return {"error": "Token is not valid!"}, 401

    user_id = payload.get("user_id")

    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found!"}, 404
    
    profile_data = {
        'user_id': user.user_id,
        'username': user.username,
        'bio': user.bio,
        'following': get_following_count(user_id),
        'followers': get_followers_count(user_id),
        'tweets': get_recent_tweets(user_id)
    }
    
    return profile_data

def get_following_count(user_id):
    following_count = Following.query.filter_by(follower_id=user_id).count()
    return following_count

def get_followers_count(user_id):
    followers_count = Following.query.filter_by(followed_user_id=user_id).count()
    return followers_count

def get_recent_tweets(user_id):
    recent_tweets = (
        Tweet.query.filter_by(user_id=user_id)
        .order_by(Tweet.published_at.desc())
        .limit(10)
        .all()
    )

    tweets_data = [{
        'id': tweet.id,
        'published_at': tweet.published_at,
        'tweet': tweet.tweet
    } for tweet in recent_tweets]

    return tweets_data


# from flask import Blueprint, request
# import jwt, os
# from user.models import User
# from auth.utils import decode_jwt

# user_blueprint = Blueprint('user', __name__)
# # user apis used after we set token & pip instal pyjwt
# # kirim query param dari header token
# @user_blueprint.route("/", methods=["GET"])
# def get_user_profile():
#     token = request.headers.get('Authorization') # for debugging purpose only
#     if not token:
#         return {"error": "Token is missing"}, 401
#     # print("Received Token:", token) # for debugging purpose only
#     # token tak boleh disimpan di cookies ataupun muncul di console
#     # DRY, utils file is exist :
#     payload = decode_jwt(token)
#     # request.headers.get('Authorization')
#     if not payload:
#         return {"error": "Token is not valid!"}, 401

#     user = User.query.get(payload["user_id"])
#     if not user:
#         return {"error": "User not found!"}, 404
    
#     return {
#         'id': user.user_id,
#         'username': user.username,
#         'bio': user.bio
#         # 'email': user.email
#     }
