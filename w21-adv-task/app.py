import os
from flask import Flask
from db import db, db_init
from common.bcrypt import bcrypt
from auth.apis import auth_blp
from user.apis import user_blueprint, moderation_blueprint
from tweet.apis import tweet_blueprint
from following.apis import following_blueprint

app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(auth_blp, url_prefix="/auth")
app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(tweet_blueprint, url_prefix="/tweet")
app.register_blueprint(following_blueprint, url_prefix="/following")
app.register_blueprint(moderation_blueprint, url_prefix="/moderation")

with app.app_context():
    db_init()

# print & breakpoint in py similar to console.log() in js

# object js = dictionary py

# user = {
#   'id':1,
#   'name': 'john'
# }

# id = user.get('id')
# id = user.id
# cors config khusus di flask