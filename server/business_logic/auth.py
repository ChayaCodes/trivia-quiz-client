import os
import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from data.database_functions_quizes import (
    get_user_by_email,
    create_user,
    generate_unique_user_id,
)

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRATION_MINUTES = 15
REFRESH_TOKEN_EXPIRATION_DAYS = 7

def register_user(username, email, password):
    """
    Registers a new user with a hashed password.

    :param username: User's name
    :param email: User's email
    :param password: User's password
    :return: Success or error message
    """
    existing_user = get_user_by_email(email)
    if existing_user:
        return {'error': 'User already exists.'}, 400

    user_id = generate_unique_user_id()
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # עדכון כאן
    create_user(user_id, username, email, hashed_password)

    return {'message': 'User registered successfully.'}, 201

def login_user(email, password):
    """
    Authenticates a user and returns JWT tokens.

    :param email: User's email
    :param password: User's password
    :return: JWT access and refresh tokens or error message
    """
    user = get_user_by_email(email)
    if not user:
        return {'error': 'User does not exist.'}, 404

    if not check_password_hash(user['password'], password):
        return {'error': 'Incorrect password.'}, 401

    access_token = generate_access_token(user['id'])
    refresh_token = generate_refresh_token(user['id'])

    return {'access_token': access_token, 'refresh_token': refresh_token}, 200



def generate_access_token(user_id):
    """
    Generates a JWT access token.

    :param user_id: ID of the user
    :return: JWT access token as a string
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES),
        'type': 'access'
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def generate_refresh_token(user_id):
    """
    Generates a JWT refresh token.

    :param user_id: ID of the user
    :return: JWT refresh token as a string
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRATION_DAYS),
        'type': 'refresh'
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token):
    """
    Decodes a JWT token.

    :param token: JWT token
    :return: Decoded payload or error
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded, None
    except jwt.ExpiredSignatureError:
        return None, 'Token has expired.'
    except jwt.InvalidTokenError:
        return None, 'Invalid token.'

def token_required(f):
    """
    Decorator that ensures the user has a valid access JWT token.
    The token is expected to be sent via cookies.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')

        if not token:
            return jsonify({'error': 'Access token is missing.'}), 401

        decoded, error = decode_token(token)
        if error:
            return jsonify({'error': error}), 401

        if decoded.get('type') != 'access':
            return jsonify({'error': 'Invalid token type.'}), 401

        user_id = decoded.get('user_id')
        if not user_id:
            return jsonify({'error': 'Token is invalid.'}), 401

        return f(user_id, *args, **kwargs)
    
    return decorated

def refresh_token_required(f):
    """
    Decorator that ensures the user has a valid refresh JWT token.
    The token is expected to be sent via cookies.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('refresh_token')

        if not token:
            return jsonify({'error': 'Refresh token is missing.'}), 401

        decoded, error = decode_token(token)
        if error:
            return jsonify({'error': error}), 401

        if decoded.get('type') != 'refresh':
            return jsonify({'error': 'Invalid token type.'}), 401

        user_id = decoded.get('user_id')
        if not user_id:
            return jsonify({'error': 'Token is invalid.'}), 401

        return f(user_id, *args, **kwargs)
    
    return decorated


def get_user_id_from_token(token):
    """
    Extracts the user ID from a JWT token.

    :param token: JWT token
    :return: User ID or None
    """
    decoded, error = decode_token(token)
    if error:
        return None

    return decoded.get('user_id')


