from datetime import datetime
from src.database.intialize_database import db, ma
from flask import current_app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)


    def __init__(self, username,password):
        self.username = username
        self.password = password










