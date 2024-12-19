from flask import Flask, request, jsonify, make_response, Blueprint
from functools import wraps
from business_logic.auth import (
    register_user,
    login_user,
    decode_token,
    token_required,
    refresh_token_required,
    generate_access_token
)
from business_logic.admin_interface import ( get_user_by_id )
import dotenv

import os

import dotenv

# Define token expiration times
ACCESS_TOKEN_EXPIRATION_MINUTES = 15  # Example value, adjust as needed
REFRESH_TOKEN_EXPIRATION_DAYS = 7  # Example value, adjust as needed

auth_api = Blueprint('auth_api', __name__)

# Load environment variables
dotenv.load_dotenv()

@auth_api.route('/auth/register', methods=['POST'])
def api_register():
    data = request.get_json()
    print(data)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'error': 'שדות חובה חסרים.'}), 400
    
    response, status = register_user(username, email, password)
    return jsonify(response), status

@auth_api.route('/auth/login', methods=['POST'])
def api_login_route():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'חסר אימייל או סיסמא.'}), 400
    
    response, status = login_user(email, password)
    if status == 200:
        access_token = response.get('access_token')
        refresh_token = response.get('refresh_token')
        
        resp = make_response(jsonify({'message': 'התחברות הצליחה.'}), status)
        
        # הגדרת הטוקנים כקוקיז HTTP-Only
        resp.set_cookie(
            'access_token',
            access_token,
            httponly=True,
            secure=True,  # ודא שהשרת רץ על HTTPS
            samesite='Strict',
            max_age=ACCESS_TOKEN_EXPIRATION_MINUTES * 60
        )
        
        resp.set_cookie(
            'refresh_token',
            refresh_token,
            httponly=True,
            secure=True,  # ודא שהשרת רץ על HTTPS
            samesite='Strict',
            max_age=REFRESH_TOKEN_EXPIRATION_DAYS * 24 * 60 * 60
        )
        
        return resp
    return jsonify(response), status

@auth_api.route('/auth/logout', methods=['POST'])
@token_required
def api_logout(user_id):
    resp = make_response(jsonify({'message': 'התנתקות מוצלחת.'}), 200)
    # מחיקת הקוקיז
    resp.set_cookie('access_token', '', expires=0)
    resp.set_cookie('refresh_token', '', expires=0)
    return resp

@auth_api.route('/auth/refresh', methods=['POST'])
@refresh_token_required
def api_refresh_token(user_id):
    """
    מסלול לחידוש טוקן הגישה באמצעות Refresh Token.
    """
    new_access_token = generate_access_token(user_id)
    
    resp = make_response(jsonify({'access_token': new_access_token}), 200)
    
    resp.set_cookie(
        'access_token',
        new_access_token,
        httponly=True,
        secure=True,  # ודא שהשרת רץ על HTTPS
        samesite='Strict',
        max_age=ACCESS_TOKEN_EXPIRATION_MINUTES * 60
    )
    
    return resp

@auth_api.route('/auth/me', methods=['GET'])
@token_required
def api_me(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'משתמש לא נמצא.'}), 404
    
    user_info = {
        'id': user['id'],
        'name': user['name'],
        'email': user['email']
    }
    return jsonify({'user': user_info}), 200