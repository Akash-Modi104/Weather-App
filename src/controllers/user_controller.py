import logging
from flask import request,session,jsonify
from src.entity.user import User
from werkzeug.security import generate_password_hash, check_password_hash

import logging

logger = logging.getLogger(__name__)

from src.database.intialize_database import db


def add_user():
    try:
        request_details = request.json
        username =request_details['username']
        password = request_details['password']
        user = User.query.filter_by(username=username).first()
        if user:
            return {"user created": "False","comment":"user already present !!! please login"}, 200
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return {"user created": "True","comment":"user created!!! please LOGIN"},201
    except Exception as e:
        logger.exception(e)
        return {"user created": "False","comment":'something went wrong!!! try again'}, 500


def login():
    try:
        request_details = request.json
        username = request_details['username']
        password = request_details['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            print(session)
            return {"login":True,"comment":"correct details"},200
        return {"login":False,"comment":'Invalid username or password'},401
    except Exception as e:
        logger.exception(e)
        return {"login":False,"comment":'something went wrong'}, 500


def logout(username):
    if 'username' in session and session['username'] == username:
        session.pop('username', None)
        return jsonify({'message': f'Logout successful for {username}'}), 200
    else:
        return jsonify({'message': 'User not logged in'}), 401


