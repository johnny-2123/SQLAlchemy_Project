from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ


class Config:
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL") or "sqlite:///dev.db"
    SQLALCHEMY_TRACK_MODIFICATION = False


flask_app = Flask(__name__)
flask_app.config.from_object(Config)
db = SQLAlchemy(flask_app)
