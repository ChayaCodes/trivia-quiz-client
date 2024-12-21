import threading
import traceback

from flask import Blueprint
from flask import jsonify, request

from data.database_functions import (
    set_data_by_id,
    get_data_list,
    set_call_data,
    set_call_data_by_id,
    get_call_data,
    get_call_data_list,
    delete_call_data,
    delete_data_by_id, get_call_data_by_id, delete_data_by_key_and_id,
)
from utils import (
    TemporaryRequest,
    wait_for_analysis_response, get_analysis_response,
    normalize_phone_number, get_similarity_results
)

from business_logic.participant_interface import (
    add_participant, 
    answer_current_question,
    get_quiz
)

quiz_service_api = Blueprint('quiz_service_api', __name__)

manager_phone = "0583241182"  # הכנס את הטלפון שלך, טלפון  זה ישמש לניהול השירות
email = "chaya41182@gmail.com"  # הכנס את האימייל שלך
base_url="http://51.84.42.17/"

# חלק הרישום של השירות
service_data = {
    'manager_phone': manager_phone,
    'email': email,
    'connection_url': base_url + "/quiz_service_service",
    'service_name': 'מערכת חידון קליקרים',
    'brief_description': 'מערכת המאפשרת להשתתף בחידון קליקרים בצורה אינטראקטיבית דרך הטלפון',
    'message': 'נא הקש את קוד החידון שמופיע על המסך',
    'audio_url': '',
    'long_explanation': 'המערכת מאפשרת להשתתף בחידונים בצורה אינטראקטיבית תוך שילוב של צפייה בשאלות במערכת הווב, והשתתפות של שחקנים רבים בו זמנית',
    'required_data_schema': {},
    'number_of_digits': 6,
    'phone_number_required': True,
    'email_required': False,
    'credit_card_required': False,
    'system_payments': False,
    'external_payments': False,
    'entry_amount_to_be_paid': 0,
    'referral_phone': '',
    'analysis_delay': 0
}


@quiz_service_api.route('/quiz_service_service', methods=['POST'])
def temporary_position_service():
    target = request.json.get('target')
    if target == 'registration':
        return jsonify(service_data), 200
    elif target == 'service_processing':
        try:
            stage = get_call_data('next_stage')
            if not stage:
                stage = 'start'
                phone_number = request.json.get('phone_number')
                if phone_number:
                    set_call_data("phone_number", normalize_phone_number(phone_number))

            return do_stage(stage)
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            return send_ending_response()

def do_stage(stage):
    # קבלת השלב מהמילון stages
    stage_data = stages.get(stage)
    if not stage_data:
        print(f"Error: stage '{stage}' not found.")
        return send_ending_response()  # אם השלב לא נמצא, נחזיר תשובה

    next_stage = stage_data.get('next_stage')
    set_call_data('next_stage', next_stage)
    # הפעלת הפעולה של השלב
    stage_data['action']()

    # קבלת השלב הבא מהמידע הגולמי או מהקריאה ל- get_call_data
    next_stage = get_call_data('next_stage')
    print(f"next_stage: {next_stage}")



    # אם אין next_stage, נסיים את הפונקציה
    if not next_stage:
        print(f"Error: next_stage not found for stage {stage}")
        return send_ending_response()

    # בניית התשובה עם הערכים המתאימים
    next_stage_data = stages.get(next_stage)
    if not next_stage_data:
        print(f"Error: next_stage '{next_stage}' not found in stages dictionary.")
        return send_ending_response()


    response = {}

    # בדוק אם כל מפתח קיים לפני הוספתו ל-response
    if 'message' in next_stage_data['object'] and callable(next_stage_data['object']['message']):
        response['message'] = next_stage_data['object']['message']()
    if 'number_of_digits' in next_stage_data['object']:
        response['number_of_digits'] = next_stage_data['object']['number_of_digits']
    if 'required_data_schema' in next_stage_data['object']:
        response['required_data_schema'] = next_stage_data['object']['required_data_schema']

    return jsonify(response), 200



def send_ending_response():
    delete_call_data()
    return jsonify({}), 200  # החזר ריק הוא הסימן לסיום השירות



def start_stage():
    phone_number = get_call_data('phone_number')
    if not phone_number:
        return send_ending_response()

    quiz_id = request.json.get('digits')
    quiz = get_quiz(quiz_id)
    print(quiz)
    if not quiz:
        return set_call_data('next_stage', 'start')

    add_participant(phone_number, quiz_id)
    set_call_data('next_stage', 'answer')

def answer_stage():
    phone_number = get_call_data('phone_number')
    if not phone_number:
        return send_ending_response()

    answer_index = request.json.get('digits')

    answer_current_question(phone_number, answer_index)


stages = {
    'start': {
        'object': {
            'message': lambda: "נא הקש את קוד החידון שמופיע על המסך",
            'number_of_digits': 6
        },
        'action': start_stage,
        'next_stage': 'answer'
    },
    'answer': {
        'object': {
            'message': lambda: "",
            'number_of_digits': 1
        },
        'action': answer_stage,
        'next_stage': 'answer'
    }
}