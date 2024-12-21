import sqlite3
import os
import random
import string
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv('DATABASE_NAME', 'quiz_system.db')

def initialize_database():
    conn = sqlite3.connect(DATABASE_NAME)
    data_cursor = conn.cursor()
    
    # Create users table
    data_cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Create quizzes table
    data_cursor.execute("""
        CREATE TABLE IF NOT EXISTS quizzes (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            user_id TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'inactive',
            current_question_id TEXT,
            question_start_time INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(current_question_id) REFERENCES questions(id)
        )
    """)
    
    # Create questions table
    data_cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id TEXT PRIMARY KEY,
            quiz_id TEXT NOT NULL,
            question_text TEXT NOT NULL,
            FOREIGN KEY(quiz_id) REFERENCES quizzes(id)
        )
    """)

    # Create options table
    data_cursor.execute("""
        CREATE TABLE IF NOT EXISTS options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id TEXT NOT NULL,
            option_text TEXT NOT NULL,
            is_correct BOOLEAN NOT NULL,
            FOREIGN KEY(question_id) REFERENCES questions(id)
        )
    """)
        
    # Create participants table
    data_cursor.execute("""
        CREATE TABLE IF NOT EXISTS participants (
            phone_number TEXT PRIMARY KEY,
            quiz_id TEXT NOT NULL,
            FOREIGN KEY(quiz_id) REFERENCES quizzes(id)
        )
    """)
    
    # Create answers table
    data_cursor.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT NOT NULL,
            question_id TEXT NOT NULL,
            selected_option INTEGER NOT NULL,
            is_correct BOOLEAN NOT NULL,
            time_taken INTEGER NOT NULL,
            FOREIGN KEY(phone_number) REFERENCES participants(phone_number),
            FOREIGN KEY(question_id) REFERENCES questions(id)
        )
    """)
    
    conn.commit()
    conn.close()

initialize_database()

def generate_unique_quiz_id(length=6):
    while True:
        new_id = ''.join(random.choices(string.digits, k=length))
        if not get_quiz(new_id):
            return new_id

def generate_unique_question_id(length=8):
    while True:
        new_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        if not get_question(new_id):
            return new_id

def generate_unique_user_id(length=8):
    while True:
        new_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        if not get_user(new_id):
            return new_id

# CRUD operations for Users
def create_user(id, name, email, password):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_cursor = data_conn.cursor()
        data_cursor.execute("""
            INSERT INTO users (id, name, email, password) VALUES (?, ?, ?, ?)
        """, (id, name, email, password))
        data_conn.commit()
    finally:
        data_conn.close()

def get_user(id):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_conn.row_factory = sqlite3.Row
        data_cursor = data_conn.cursor()
        data_cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        row = data_cursor.fetchone()
        if row:
            return dict(row)
        return None
    finally:
        data_conn.close()

def get_user_by_email(email):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_conn.row_factory = sqlite3.Row
        data_cursor = data_conn.cursor()
        data_cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = data_cursor.fetchone()
        if row:
            return dict(row)
        return None
    finally:
        data_conn.close()

def get_user_by_username(name):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_conn.row_factory = sqlite3.Row
        data_cursor = data_conn.cursor()
        data_cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        row = data_cursor.fetchone()
        if row:
            return dict(row)
        return None
    finally:
        data_conn.close()

def update_user(id, name=None, email=None, password=None):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_cursor = data_conn.cursor()
        if name:
            data_cursor.execute("UPDATE users SET name = ? WHERE id = ?", (name, id))
        if email:
            data_cursor.execute("UPDATE users SET email = ? WHERE id = ?", (email, id))
        if password:
            data_cursor.execute("UPDATE users SET password = ? WHERE id = ?", (password, id))
        data_conn.commit()
    finally:
        data_conn.close()

def delete_user(id):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_cursor = data_conn.cursor()
        data_cursor.execute("DELETE FROM users WHERE id = ?", (id,))
        data_conn.commit()
    finally:
        data_conn.close()

# CRUD operations for Quizzes
def create_quiz(id, name, user_id):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_cursor = data_conn.cursor()
        data_cursor.execute("""
            INSERT INTO quizzes (id, name, user_id, status) VALUES (?, ?, ?, 'inactive')
        """, (id, name, user_id))
        data_conn.commit()
    finally:
        data_conn.close()

def get_quiz(id: str) -> dict:
    """
    Retrieves quiz details by ID.

    :param id: מזהה החידון.
    :return: מילון עם פרטי החידון או None אם לא נמצא.
    """
    data_conn = None
    try:
        data_conn = sqlite3.connect(os.getenv('DATABASE_NAME'))
        data_conn.row_factory = sqlite3.Row
        data_cursor = data_conn.cursor()
        data_cursor.execute("SELECT * FROM quizzes WHERE id = ?", (id,))
        row = data_cursor.fetchone()
        if row:
            return dict(row)
        return None
    except sqlite3.Error as e:
        return {}
    finally:
        if data_conn:
            data_conn.close()


def update_quiz(id, name=None, user_id=None, status=None, current_question_id=None, question_start_time=None):
    """
    Updates quiz details.

    :param id: מזהה החידון.
    :param name: שם החידון (אופציונלי).
    :param user_id: מזהה המשתמש (אופציונלי).
    :param status: סטטוס החידון (אופציונלי).
    :param current_question_id: מזהה השאלה הנוכחית (אופציונלי).
    :param question_start_time: זמן התחלת השאלה (אופציונלי).
    """
    try:
        with sqlite3.connect(DATABASE_NAME) as data_conn:
            data_cursor = data_conn.cursor()
            if name:
                data_cursor.execute("UPDATE quizzes SET name = ? WHERE id = ?", (name, id))
            if user_id:
                data_cursor.execute("UPDATE quizzes SET user_id = ? WHERE id = ?", (user_id, id))
            if status:
                data_cursor.execute("UPDATE quizzes SET status = ? WHERE id = ?", (status, id))
            if current_question_id:
                data_cursor.execute("UPDATE quizzes SET current_question_id = ? WHERE id = ?", (current_question_id, id))
            if question_start_time is not None:
                data_cursor.execute("UPDATE quizzes SET question_start_time = ? WHERE id = ?", (question_start_time, id))
            data_conn.commit()
    except sqlite3.Error as e:
        logger.error(f"שגיאה במסד הנתונים במהלך עדכון החידון: {e}")
    except Exception as e:
        logger.error(f"שגיאה בלתי צפויה במהלך עדכון החידון: {e}")

def delete_quiz(id):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_cursor = data_conn.cursor()
        data_cursor.execute("DELETE FROM quizzes WHERE id = ?", (id,))
        data_conn.commit()
    finally:
        data_conn.close()

# CRUD operations for Questions
def create_question(id, quiz_id, question_text):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_cursor = data_conn.cursor()
        data_cursor.execute("""
            INSERT INTO questions (id, quiz_id, question_text) VALUES (?, ?, ?)
        """, (id, quiz_id, question_text))
        data_conn.commit()
    finally:
        data_conn.close()

def get_question(id):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_conn.row_factory = sqlite3.Row
        data_cursor = data_conn.cursor()
        data_cursor.execute("SELECT * FROM questions WHERE id = ?", (id,))
        row = data_cursor.fetchone()
        if row:
            return dict(row)
        return None
    finally:
        data_conn.close()

def get_questions(quiz_id: str) -> list[dict]:
    """
    Retrieves all questions for a given quiz.

    :param quiz_id: מזהה החידון.
    :return: רשימת שאלות.
    """
    try:
        with sqlite3.connect(DATABASE_NAME) as data_conn:
            data_conn.row_factory = sqlite3.Row
            data_cursor = data_conn.cursor()
            data_cursor.execute("SELECT * FROM questions WHERE quiz_id = ?", (quiz_id,))
            rows = data_cursor.fetchall()
            if rows:
                return [dict(row) for row in rows]  # תיקון הלולאה
            return []
    except sqlite3.Error as e:
        return []
    except Exception as e:
        return []
    finally:
        if data_conn:
            data_conn.close()

def update_question(id, quiz_id=None, question_text=None):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_cursor = data_conn.cursor()
        if quiz_id:
            data_cursor.execute("UPDATE questions SET quiz_id = ? WHERE id = ?", (quiz_id, id))
        if question_text:
            data_cursor.execute("UPDATE questions SET question_text = ? WHERE id = ?", (question_text, id))
        data_conn.commit()
    finally:
        data_conn.close()

def delete_question(id):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_cursor = data_conn.cursor()
        data_cursor.execute("DELETE FROM questions WHERE id = ?", (id,))
        data_conn.commit()
    finally:
        data_conn.close()

# CRUD operations for Options
def create_option(question_id, option_text, is_correct):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_cursor = data_conn.cursor()
        data_cursor.execute("""
            INSERT INTO options (question_id, option_text, is_correct) VALUES (?, ?, ?)
        """, (question_id, option_text, is_correct))
        data_conn.commit()
    finally:
        data_conn.close()

def get_options_by_question(question_id):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_conn.row_factory = sqlite3.Row
        data_cursor = data_conn.cursor()
        data_cursor.execute("SELECT * FROM options WHERE question_id = ?", (question_id,))
        rows = data_cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        data_conn.close()

# CRUD operations for Participants
def create_participant(phone_number, quiz_id):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_cursor = data_conn.cursor()
        data_cursor.execute("""
            INSERT INTO participants (phone_number, quiz_id) VALUES (?, ?)
        """, (phone_number, quiz_id))
        data_conn.commit()
    finally:
        data_conn.close()

def get_participant(phone_number):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_conn.row_factory = sqlite3.Row
        data_cursor = data_conn.cursor()
        data_cursor.execute("SELECT * FROM participants WHERE phone_number = ?", (phone_number,))
        row = data_cursor.fetchone()
        if row:
            return dict(row)
        return None
    finally:
        data_conn.close()

def delete_participant(phone_number):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_cursor = data_conn.cursor()
        data_cursor.execute("DELETE FROM participants WHERE phone_number = ?", (phone_number,))
        data_conn.commit()
    finally:
        data_conn.close()

# CRUD operations for Participant Answers
def add_participant_answer(participant_phone, question_id, selected_option, is_correct, time_taken):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_cursor = data_conn.cursor()
        data_cursor.execute("""
            INSERT INTO answers (phone_number, question_id, selected_option, is_correct, time_taken) 
            VALUES (?, ?, ?, ?, ?)
        """, (participant_phone, question_id, selected_option, is_correct, time_taken))
        data_conn.commit()
    finally:
        data_conn.close()

def get_participant_answers(participant_phone):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_conn.row_factory = sqlite3.Row
        data_cursor = data_conn.cursor()
        data_cursor.execute("SELECT * FROM answers WHERE phone_number = ?", (participant_phone,))
        rows = data_cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        data_conn.close()

def update_participant_answer(participant_phone, question_id, selected_option=None, is_correct=None, time_taken=None):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_cursor = data_conn.cursor()
        if selected_option is not None:
            data_cursor.execute("UPDATE answers SET selected_option = ? WHERE phone_number = ? AND question_id = ?", (selected_option, participant_phone, question_id))
        if is_correct is not None:
            data_cursor.execute("UPDATE answers SET is_correct = ? WHERE phone_number = ? AND question_id = ?", (is_correct, participant_phone, question_id))
        if time_taken is not None:
            data_cursor.execute("UPDATE answers SET time_taken = ? WHERE phone_number = ? AND question_id = ?", (time_taken, participant_phone, question_id))
        data_conn.commit()
    finally:
        data_conn.close()

def delete_participant_answer(participant_phone, question_id):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_cursor = data_conn.cursor()
        data_cursor.execute("DELETE FROM answers WHERE phone_number = ? AND question_id = ?", (participant_phone, question_id))
        data_conn.commit()
    finally:
        data_conn.close()


def get_current_question(quiz_id):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_cursor = data_conn.cursor()
        data_cursor.execute("SELECT current_question_id FROM quizzes WHERE id = ?", (quiz_id,))
        row = data_cursor.fetchone()
        if row:
            return row[0]
        return None
    finally:
        data_conn.close()


def get_quizzes_by_user(user_id):
    try:
        data_conn = sqlite3.connect(DATABASE_NAME)
        data_conn.row_factory = sqlite3.Row
        data_cursor = data_conn.cursor()
        data_cursor.execute("SELECT name, id FROM quizzes WHERE user_id = ?", (user_id,))
        rows = data_cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        data_conn.close()

def get_all_participants(quiz_id):
    """
    Retrieves all participants for a given quiz.
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM participants WHERE quiz_id = ?", (quiz_id,))
        rows = cursor.fetchall()
        participants = [dict(row) for row in rows]
        return participants
    except sqlite3.Error as e:
        print(f"Database error in get_all_participants: {e}")
        return []
    finally:
        conn.close()