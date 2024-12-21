from flask import Blueprint, request, jsonify
from flask_cors import CORS
from business_logic.admin_interface import (
    create_new_quiz,
    edit_quiz,
    activate_quiz,
    get_quiz_statistics,
    view_quizzes,
    get_current_active_question,
    go_to_next_question,
    get_participants
)
import dotenv

from api.auth_api import token_required

quizzes_interface_api = Blueprint('admin_api', __name__)

CORS(quizzes_interface_api, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# Load environment variables
dotenv.load_dotenv()

@quizzes_interface_api.route('/admin/create_quiz', methods=['POST'])
@token_required
def api_create_quiz(user_id):
    try:
        data = request.get_json()
        print("Received quiz data:", data)  # הדפס נתונים ללוג

        title = data.get('title')
        questions = data.get('questions')


        if not title or not questions:
            print("Missing title or questions")
            return jsonify({'error': 'שדות חובה חסרים.'}), 400

        # ודא ש-create_new_quiz מקבל את כל הפרמטרים הנדרשים
        response, status = create_new_quiz(title, user_id, questions)
        return jsonify(response), status
    except Exception as e:
        print("Error in api_create_quiz:", str(e))
        return jsonify({'error': 'שגיאה בשרת.'}), 500

@quizzes_interface_api.route('/admin/edit_quiz/<quiz_id>', methods=['PUT'])
@token_required
def api_edit_quiz(user_id, quiz_id):
    data = request.get_json()
    name = data.get('name')
    questions = data.get('questions')
    correct_options = data.get('correct_options')
    
    response, status = edit_quiz(quiz_id=quiz_id, user_id=user_id, name=name, questions=questions, correct_options=correct_options)
    return jsonify(response), status

@quizzes_interface_api.route('/admin/activate_quiz/<quiz_id>', methods=['POST'])
@token_required
def api_activate_quiz(user_id, quiz_id):
    response, status = activate_quiz(quiz_id=quiz_id, user_id=user_id)
    return jsonify(response), status

@quizzes_interface_api.route('/admin/view_quizzes', methods=['GET'])
@token_required
def api_view_quizzes(user_id):
    response, status = view_quizzes(user_id)
    return jsonify(response), status

@quizzes_interface_api.route('/admin/quiz_statistics/<quiz_id>', methods=['GET'])
@token_required
def api_quiz_statistics(user_id, quiz_id):
    response, status = get_quiz_statistics(quiz_id=quiz_id, user_id=user_id)
    return jsonify(response), status



@quizzes_interface_api.route('/admin/get_current_question/<quiz_id>', methods=['GET'])
@token_required
def api_get_current_question(user_id, quiz_id):
    response, status = get_current_active_question(quiz_id)
    return jsonify(response), status

# New Endpoint: Go to Next Question
@quizzes_interface_api.route('/admin/go_to_next_question/<quiz_id>', methods=['POST'])
@token_required
def api_go_to_next_question(user_id, quiz_id):
    response, status = go_to_next_question(quiz_id)
    return jsonify(response), status



# New Endpoint: Get Participants of a Quiz
@quizzes_interface_api.route('/admin/get_participants/<quiz_id>', methods=['GET'])
@token_required
def api_get_participants(user_id, quiz_id):
    response, status = get_participants(quiz_id)
    return jsonify(response), status