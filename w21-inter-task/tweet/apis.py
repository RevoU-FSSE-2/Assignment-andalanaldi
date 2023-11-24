from flask import Blueprint, request
from datetime import datetime
# from tweet.constants import EVENT_DATE_FORMAT
# import jwt, os
from user.models import User
from tweet.models import Tweet
from auth.utils import decode_jwt
# from common.bcrypt import bcrypt
from db import db

tweet_blueprint = Blueprint("tweet", __name__)

@tweet_blueprint.route("/", methods=["POST"])
def post_tweet():
    data = request.get_json()
    token = request.headers.get('Authorization') # for debugging purpose only
    if not token:
        return {"error": "Token is missing"}, 401

    payload = decode_jwt(token)
    if not payload:
        return {"error": "Token is not valid!"}, 401

    user_id = payload.get("user_id")  # Retrieve user ID from the token payload

    tweet_content = data.get("tweet")
    if not tweet_content:
        return {"error": "Tweet content is missing"}, 400

    if len(tweet_content) > 150:
        return {"error": "Tweet cannot exceed 150 characters"}, 400

    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found!"}, 404

    # Generate the published_at timestamp
    published_at = datetime.utcnow()

    # Create a new tweet
    new_tweet = Tweet(user_id=user_id, published_at=published_at, tweet=tweet_content)
    db.session.add(new_tweet)
    db.session.commit()
   
    return {
        'id': new_tweet.id,
        'published_at': new_tweet.published_at,
        'tweet': new_tweet.tweet
    }
