from flask import Flask, request, jsonify, make_response, Blueprint
from functools import wraps
from business_logic.auth import register_user, login_user, decode_token
from data.database_functions_quizes import get_user, create_user
import dotenv

# Load environment variables
dotenv.load_dotenv()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({'error': 'Token is missing.'}), 401
        
        user_id, error = decode_token(token)
        if error:
            return jsonify(error), 401
        
        return f(user_id, *args, **kwargs)
    
    return decorated

auth_api = Blueprint('auth_api', __name__)

@auth_api.route('/auth/register', methods=['POST'])
def api_register():
    data = request.get_json()
    name = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not name or not email or not password:
        return jsonify({'error': 'Missing required fields.'}), 400
    
    response, status = register_user(name, email, password)
    if status == 201:
        token = response.get('token')
        resp = make_response(jsonify({'message': 'Login successful.'}), status)
        resp.set_cookie('token', token, httponly=True, samesite='Strict')
        return resp
    return jsonify(response), status


@auth_api.route('/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(data)
    if not username or not password:
        return jsonify({'error': 'Missing username or password.'}), 400
    
    response, status = login_user(username, password)
    if status == 200:
        token = response.get('token')
        resp = make_response(jsonify({'message': 'Login successful.'}), status)
        resp.set_cookie('token', token, httponly=True, samesite='Strict')
        return resp
    return jsonify(response), status

@auth_api.route('/auth/logout', methods=['POST'])
@token_required
def api_logout(user_id):
    resp = make_response(jsonify({'message': 'Logged out successfully.'}), 200)
    resp.set_cookie('token', '', expires=0)
    return resp

@auth_api.route('/auth/me', methods=['GET'])
@token_required
def api_me(user_id):
    user = get_user_by_id(user_id) # type: ignore
    if not user:
        return jsonify({'error': 'User not found.'}), 404
    
    user_info = {
        'id': user['id'],
        'name': user['name'],
        'email': user['email']
    }
    return jsonify({'user': user_info}), 200

