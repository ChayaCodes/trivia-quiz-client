from data.database_functions_quizes import (
    create_quiz,
    get_quiz,
    update_quiz,
    delete_quiz,
    create_question,
    get_user,
    get_question,
    generate_unique_question_id,
    generate_unique_quiz_id,
    create_option,
    get_participant_answers
)
import time
import sqlite3
import os

import sqlite3

DB_NAME = 'quizzes_data.db'


def create_new_quiz(title, user_id, questions):
    """
    Creates a new quiz with questions and single correct answer.
    """
    try:
        # התחברות למסד הנתונים
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # יצירת ID ייחודי לחידון
        quiz_id = generate_unique_quiz_id()

        # הכנסת החידון לטבלה הראשית
        cursor.execute("""
            INSERT INTO quizzes (id, name, user_id, status) 
            VALUES (?, ?, ?, 'active')
        """, (quiz_id, title, user_id))

        # הכנסת השאלות והתשובות לטבלאות המתאימות
        for q in questions:
            q_text = q.get('question')
            answers = q.get('answers')  # מערך של מחרוזות
            correct_answer = q.get('correctAnswer')  # מחרוזת

            # בדיקה שהשאלה כוללת תשובה נכונה בתוך אפשרויות התשובות
            if correct_answer not in answers:
                conn.close()
                return {'error': f'תשובה נכונה "{correct_answer}" אינה קיימת באפשרויות התשובות לשאלה "{q_text}".'}, 400

            # יצירת ID ייחודי לשאלה
            question_id = generate_unique_question_id()

            # הכנסת השאלה לטבלה ללא `correct_answer`
            cursor.execute("""
                INSERT INTO questions (id, quiz_id, question_text)
                VALUES (?, ?, ?)
            """, (question_id, quiz_id, q_text))

            # הכנסת התשובות לטבלה עם הגדרת `is_correct`
            for answer_text in answers:
                is_correct = 1 if answer_text == correct_answer else 0
                cursor.execute("""
                    INSERT INTO options (question_id, option_text, is_correct)
                    VALUES (?, ?, ?)
                """, (question_id, answer_text, is_correct))

        # אישור השינויים וסגירת החיבור
        conn.commit()
        conn.close()

        return {'message': 'חידון נוצר בהצלחה.', 'quiz_id': quiz_id}, 201
    except sqlite3.Error as e:
        print("Database error in create_new_quiz:", e)
        return {'error': 'שגיאה במסד הנתונים.'}, 500
    except Exception as e:
        print("Error in create_new_quiz:", e)
        return {'error': 'שגיאה ביצירת החידון.'}, 500


def view_quizzes(user_id):
    """
    Retrieves all quizzes created by a user.
    """
    user = get_user(user_id)
    if not user:
        return {'error': 'User not found.'}, 404
    try:
        data_conn = sqlite3.connect(os.getenv('DATABASE_NAME'))
        data_conn.row_factory = sqlite3.Row
        data_cursor = data_conn.cursor()
        data_cursor.execute("SELECT * FROM quizzes WHERE user_id = ?", (user_id,))
        rows = data_cursor.fetchall()
        quizzes = [dict(row) for row in rows]
        return {'quizzes': quizzes}, 200
    finally:
        data_conn.close()

def edit_quiz(quiz_id, user_id, name=None, questions=None):
    """
    Edits an existing quiz's details and questions.
    """
    quiz = get_quiz(quiz_id)
    if not quiz:
        return {'error': 'Quiz not found.'}, 404
    update_quiz(quiz_id, name=name)
    if questions:
        for question in questions:
            q_text = question.get('question_text')
            options = question.get('options')
            correct_options = question.get('correct_options')  # List of correct option indices
            question_id = generate_unique_question_id()
            create_question(question_id, quiz_id, q_text)
            for idx, option_text in enumerate(options, start=1):
                is_correct = idx in correct_options
                create_option(question_id, option_text, is_correct)
    return {'message': 'Quiz updated successfully.'}, 200

def activate_quiz(quiz_id, user_id):
    """
    Activates a quiz.
    """
    quiz = get_quiz(quiz_id)
    if not quiz:
        return {'error': 'Quiz not found.'}, 404
    update_quiz(quiz_id, status='active')
    return {'message': 'Quiz activated successfully.'}, 200

def go_to_next_question(quiz_id):
    """
    Moves the quiz to the next question.
    """
    quiz = get_quiz(quiz_id)
    if not quiz:
        return {'error': 'Quiz not found.'}, 404

    current_question_id = quiz['current_question_id']
    data_conn = sqlite3.connect(os.getenv('DATABASE_NAME'))
    data_cursor = data_conn.cursor()
    data_cursor.execute("""
        SELECT id FROM questions WHERE quiz_id = ? ORDER BY id
    """, (quiz_id,))
    questions = data_cursor.fetchall()
    question_ids = [q[0] for q in questions]

    if current_question_id and current_question_id in question_ids:
        current_index = question_ids.index(current_question_id)
        next_index = current_index + 1
        if next_index < len(question_ids):
            next_question_id = question_ids[next_index]
        else:
            next_question_id = None
    else:
        next_question_id = question_ids[0] if question_ids else None

    update_quiz(quiz_id, current_question_id=next_question_id, question_start_time=int(time.time()) if next_question_id else None)

    if not next_question_id:
        update_quiz(quiz_id, status='inactive')

    data_conn.close()
    return {'message': 'Moved to next question.'}, 200

def get_quiz_statistics(quiz_id, user_id):
    """
    Retrieves statistics for a specific quiz.
    """
    quiz = get_quiz(quiz_id)
    if not quiz:
        return {'error': 'Quiz not found.'}, 404

    # Fetch participants and their answers
    participants = get_all_participants(quiz_id)
    stats = []
    for participant in participants:
        answers = get_participant_answers(participant['phone_number'])
        score = calculate_score(answers)
        stats.append({
            'phone_number': participant['phone_number'],
            'score': score
        })
    return {'statistics': stats}, 200

def get_all_participants(quiz_id):
    """
    Retrieves all participants for a given quiz.
    """
    try:
        conn = sqlite3.connect(os.getenv('DATABASE_NAME'))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT phone_number FROM participants WHERE quiz_id = ?", (quiz_id,))
        rows = cursor.fetchall()
        return [{'phone_number': row['phone_number']} for row in rows]
    finally:
        conn.close()

def calculate_score(answers):
    """
    Calculates the score based on participant's answers.
    """
    score = 0
    first_correct = {}
    ordered_answers = sorted(answers, key=lambda x: x['time_taken'])

    for answer in ordered_answers:
        if answer['is_correct']:
            score += 10
            q_id = answer['question_id']
            if q_id not in first_correct:
                first_correct[q_id] = 1
                score += 10
            elif first_correct[q_id] < 3:
                first_correct[q_id] += 1
                score += 5
    return score


def get_user_by_id(user_id):
    """
    Retrieves a user by ID.
    """
    return get_user(user_id)