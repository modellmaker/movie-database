import os
from sqla_wrapper import SQLAlchemy
from sqlalchemy.pool import StaticPool

# db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))

db = SQLAlchemy(os.getenv("DATABASE_URL", 'sqlite:///localhost.sqlite'), connect_args={'check_same_thread': False},
                poolclass=StaticPool)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    session_token = db.Column(db.String)


class MovieDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    summary = db.Column(db.String)
    imdb = db.Column(db.String)
    rating = db.Column(db.Float)
    length = db.Column(db.String)
    season = db.Column(db.Integer)
    verdict = db.Column(db.String)
