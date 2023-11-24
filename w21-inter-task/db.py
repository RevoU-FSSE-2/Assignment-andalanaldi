from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def db_init():
    db.drop_all()
    db.create_all()

# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# def db_init():
#     db.drop_all()
#     db.create_all()
