import os
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify
from dotenv import load_dotenv
from data.database_functions_quizes import get_user, create_user, generate_unique_user_id, get_user_by_email

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
ALGORITHM = 'HS256'
TOKEN_EXPIRATION_MINUTES = 30

def register_user(name, email, password):
    """
    Registers a new user with a hashed password.
    
    :param name: User's name
    :param email: User's email
    :param password: User's password
    :return: Success or error message
    """
    existing_user = get_user(email)
    if existing_user:
        return {'error': 'User already exists.'}, 400
    
    hashed_password = generate_password_hash(password)
    user_id = generate_unique_user_id()
    create_user(user_id, name, email, hashed_password)
    return {'message': 'User registered successfully.'}, 201

def login_user(email, password):
    """
    Authenticates a user and returns a JWT token.
    
    :param email: User's email
    :param password: User's password
    :return: JWT token or error message
    """
    user = get_user_by_email(email)
    
    if not user or not check_password_hash(user['password'], password):
        return {'error': 'Invalid credentials.'}, 401
    
    token = generate_token(user['id'])
    return {'message': 'Login successful.', 'token': token}, 200

def generate_token(user_id):
    """
    Generates a JWT token for a given user ID.
    
    :param user_id: User's unique identifier
    :return: JWT token as a string
    """
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    payload = {
        'user_id': user_id,
        'exp': expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token):
    """
    Decodes a JWT token to retrieve the user ID.
    
    :param token: JWT token
    :return: User ID or error message
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload['user_id'], None
    except jwt.ExpiredSignatureError:
        return None, {'error': 'Token has expired.'}
    except jwt.InvalidTokenError:
        return None, {'error': 'Invalid token.'}
    

def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        
        if not token:
            return jsonify({'error': 'Token is missing.'}), 401
        
        user_id, error = decode_token(token)
    
        if error:
            return jsonify(error), 401
        
        return f(user_id, *args, **kwargs)
        
    wrapper.__name__ = f.__name__
    return wrapper