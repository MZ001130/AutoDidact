from __future__ import annotations
import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


# --------------------------------------------------
# Configuration
# --------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///" + os.path.join(BASE_DIR, "studypod.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)

# --------------------------------------------------
# MODELS
# --------------------------------------------------
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(30), primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    folders: Mapped[List["folder"]] = relationship()

class folder(db.Model):
    __tablename__ = 'folder'
    id = db.Column(db.String(30), primary_key=True)
    title = db.Column(db.String(120), unique=False, nullable=False)
    user_id = db.Column(db.String(30), ForeignKey('user.id'), nullable=False)
    subfolder: Mapped[List["subfolder"]] = relationship()

class subfolder(db.Model):
    __tablename__ = 'subfolder'
    id = db.Column(db.String(30), primary_key=True)
    title = db.Column(db.String(120), unique=False, nullable=False)
    folder_id = db.Column(db.String(30), ForeignKey('folder.id'), nullable=False)
    deck: Mapped[List["deck"]] = relationship()

class deck(db.Model):
    __tablename__ = 'deck'
    id = db.Column(db.String(30), primary_key=True)
    title = db.Column(db.String(120), unique=False, nullable=False)
    subfolder_id = db.Column(db.String(30), ForeignKey('subfolder.id'), nullable=False)
    cards: Mapped[List["card"]] = relationship()

class card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.String(30), primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    deck_id = db.Column(db.String(30), ForeignKey('deck.id'), nullable=False)


