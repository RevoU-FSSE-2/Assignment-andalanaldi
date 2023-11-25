from flask import Blueprint, request
from user.models import User
from tweet.models import Tweet
from following.models import Following
from auth.utils import decode_jwt
from db import db
import jwt, os

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

@user_blueprint.route("/feed", methods=["GET"])
def get_user_feed():
    token = request.headers.get('Authorization')
    if not token:
        return {"error": "Token is missing"}, 401

    payload = decode_jwt(token)
    if not payload:
        return {"error": "Token is not valid!"}, 401

    user_id = payload.get("user_id")

    # Fetch tweets from followed users
    tweets = get_followed_users_tweets(user_id)

    return {"tweets": tweets}

def get_followed_users_tweets(user_id):
    # Query to retrieve tweets from followed users
    followed_users_tweets = (
        Tweet.query.join(Following, Following.followed_user_id == Tweet.user_id)
        .filter(Following.follower_id == user_id)
        .order_by(Tweet.published_at.desc())
        .limit(10)
        .all()
    )

    tweets_data = [{
        'id': tweet.id,
        'user_id': tweet.user_id,
        'username': tweet.user.username,  # Add the username of the tweet author
        'published_at': tweet.published_at,
        'tweet': tweet.tweet
    } for tweet in followed_users_tweets]

    return tweets_data

# Include the token generation function for a moderator
def get_user_role(user_id):
    # Logic to retrieve the user's role from the database based on user_id
    # Modify this function to fetch the user's role from the User table
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        return user.role
    return None  # Return None if user not found or role not defined

def generate_jwt_token(user_id):
    user_role = get_user_role(user_id)
    payload = {
        'user_id': user_id,
        'role': user_role,  # Include the user's role in the payload
        # Other payload data...
    }
    # Generate JWT token with the payload using the SECRET_KEY from .env
    secret_key = os.getenv("SECRET_KEY")
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

moderation_blueprint = Blueprint('moderation', __name__)

@moderation_blueprint.route("/user", methods=["POST"])
def suspend_user():
    token = request.headers.get('Authorization')
    if not token:
        return {"error": "Token is missing"}, 401

    payload = decode_jwt(token)
    # print(payload)  # Check the payload received
    if not payload:
        return {"error": "Token is not valid!"}, 401

    user_role = get_user_role(payload.get('user_id'))
    if user_role != 'MODERATOR':
        return {"error": "User cannot do this action"}, 403
    
    data = request.get_json()
    user_id = data.get("user_id")
    is_suspended = data.get("is_suspended")

    user = User.query.get(user_id)
    if not user:
        return {"error": "User is not found"}, 404

    user.is_suspended = is_suspended
    db.session.commit()

        # Include token generation for response
    generated_token = generate_jwt_token(payload.get('user_id'))

    return {
        "user_id": user_id,
        "is_suspended": is_suspended,
        "new_token": generated_token  # Sending a new token as a response
    }
