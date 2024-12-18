from flask import request as flask_request
import sqlite3

def initialize_db():
    """
    Initialize the database by creating tables 'data' and 'call_data' if they do not exist.

    'data' table uses a composite primary key (route_id, id, key).
    'call_data' table uses a composite primary key (route_id, id, key, call_id).
    """
    try:
        data_conn = sqlite3.connect('data.db')
        data_cursor = data_conn.cursor()
        
        data_cursor.execute("""CREATE TABLE IF NOT EXISTS data (
                route_id TEXT,
                call_id  TEXT,
                local_id TEXT, 
                key TEXT, 
                value TEXT, 
                id TEXT, 
                date INTEGER,
                PRIMARY KEY (route_id, id, key)
        )""")

        data_cursor.execute("""CREATE TABLE IF NOT EXISTS call_data (
                route_id TEXT,
                call_id  TEXT,
                local_id TEXT, 
                key TEXT, 
                value TEXT, 
                id TEXT, 
                date INTEGER,
                PRIMARY KEY (route_id, id, key, call_id)
        )""")
        data_conn.commit()
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
    finally:
        data_conn.close()

def set_data_by_id(key, id, value, request=flask_request):
    """
    Insert or update a record in the 'data' table using route_id, id, key, and value.
    
    If a record with the same composite key (route_id, id, key) exists, update the value and other fields.
    """
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        route_id = request.json.get('route_id')
        call_id = request.json.get('call_id')
        local_id = request.json.get('local_id')
        
        cursor.execute("""
            INSERT INTO data (route_id, call_id, local_id, key, value, id, date) 
            VALUES (?, ?, ?, ?, ?, ?, strftime('%s','now'))
            ON CONFLICT(route_id, id, key) DO UPDATE 
            SET value = excluded.value, 
                call_id = excluded.call_id,
                local_id = excluded.local_id,
                date = strftime('%s','now')
        """, (route_id, call_id, local_id, key, value, id))
        
        conn.commit()
        return {"status": "success", "message": "Data set successfully"}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Failed to set data: {e}"}
    finally:
        conn.close()


def get_data_by_id(key, id, request=flask_request):
    """
    Retrieve a value from the 'data' table using route_id, key, and id.
    """
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        route_id = request.json.get('route_id')
        cursor.execute("SELECT value FROM data WHERE route_id = ? AND key = ? AND id = ?", (route_id, key, id))
        row = cursor.fetchone()
        return row[0] if row else None
    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")
        return None
    finally:
        conn.close()



def set_call_data_by_id(key, id, value, request=flask_request):
    """
    Insert or update a record in the 'call_data' table using route_id, id, key, and value.
    
    If a record with the same composite key (route_id, id, key, call_id) exists, update the value and other fields.
    """
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        route_id = request.json.get('route_id')
        call_id = request.json.get('call_id')
        local_id = request.json.get('local_id')
        
        cursor.execute("""
            INSERT INTO call_data (route_id, call_id, local_id, key, value, id, date) 
            VALUES (?, ?, ?, ?, ?, ?, strftime('%s','now'))
            ON CONFLICT(route_id, id, key, call_id) DO UPDATE 
            SET value = excluded.value, 
                local_id = excluded.local_id,
                date = strftime('%s','now')
        """, (route_id, call_id, local_id, key, value, id))
        
        conn.commit()
        return {"status": "success", "message": "Call data set successfully"}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Failed to set call data: {e}"}
    finally:
        conn.close()

def get_call_data_by_id(key, id, request=flask_request):
    """
    Retrieve a value from the 'call_data' table using route_id, key, and id.
    """
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        route_id = request.json.get('route_id')
        call_id = request.json.get('call_id')
        cursor.execute("SELECT value FROM call_data WHERE route_id = ? AND key = ? AND call_id = ? AND id = ?", (route_id, key,call_id, id))
        row = cursor.fetchone()
        return row[0] if row else None
    except sqlite3.Error as e:
        print(f"Error fetching call data: {e}")
        return None
    finally:
        conn.close()


def get_data_list(key, request=flask_request):
    """
    Retrieve a list of dictionaries from the 'data' table for a given route_id and key,
    where each dictionary has 'id' as the key and 'value' as the value.
    """
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        route_id = request.json.get('route_id')
        cursor.execute("SELECT id, value FROM data WHERE route_id = ? AND key = ?", (route_id, key))
        rows = cursor.fetchall()
        # יצירת רשימת מילונים עם id בתור המפתח ו-value בתור הערך
        result = [{row[0]: row[1]} for row in rows]
        return result
    except sqlite3.Error as e:
        print(f"Error fetching data list: {e}")
        return []
    finally:
        conn.close()

def get_call_data_list(key, request=flask_request):
    """
    Retrieve a list of dictionaries from the 'call_data' table for a given route_id, call_id, and key,
    where each dictionary has 'id' as the key and 'value' as the value.
    """
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        route_id = request.json.get('route_id')
        call_id = request.json.get('call_id')
        cursor.execute(
            "SELECT id, value FROM call_data WHERE route_id = ? AND call_id = ? AND key = ?",
            (route_id, call_id, key)
        )
        rows = cursor.fetchall()
        # יצירת רשימת מילונים עם id בתור המפתח ו-value בתור הערך
        result = [{row[0]: row[1]} for row in rows]
        return result
    except sqlite3.Error as e:
        print(f"Error fetching call data list: {e}")
        return []
    finally:
        conn.close()

def delete_call_data(request=flask_request):
    """
    Delete all records in the 'call_data' table based on route_id and call_id obtained from the request.
    """
    try:
        route_id = request.json.get('route_id')
        call_id = request.json.get('call_id')
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM call_data WHERE route_id = ? AND call_id = ?", (route_id, call_id))
        conn.commit()
        return {"status": "success", "message": "Call data deleted successfully"}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Failed to delete call data: {e}"}
    finally:
        conn.close()
def set_data(key, value, request=flask_request):
    """
    Insert or update a record in the 'data' table using route_id, key, and value.
    """
    return set_data_by_id(key, "", value, request)


def get_data(key, request=flask_request):
    """
    Insert or update a record in the 'data' table using route_id, key, and value.
    """
    return get_data_by_id(key, "", request)


def set_call_data(key, value, request=flask_request):
    """
    Insert or update a record in the 'data' table using route_id, key, and value.
    """
    return set_call_data_by_id(key, "", value, request)


def get_call_data(key, request=flask_request):
    """
    Insert or update a record in the 'data' table using route_id, key, and value.
    """
    return get_call_data_by_id(key, "", request)


def delete_data_by_key_and_id(key, id, request=flask_request):
    """
    Delete a record in the 'data' table based on route_id, key, and id obtained from the request.
    """
    try:
        route_id = request.json.get('route_id')
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM data WHERE route_id = ? AND key = ? AND id = ?", (route_id, key, id))
        conn.commit()
        return {"status": "success", "message": "Data deleted successfully by id"}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Failed to delete data by id: {e}"}
    finally:
        conn.close()

def delete_data_by_key(key, request=flask_request):
    """
    Delete a record in the 'data' table based on route_id, key, obtained from the request.
    """
    delete_data_by_key_and_id(key,"", request)

def delete_data_by_id(id, request=flask_request):
    """
    Delete a record in the 'data' table based on route_id and id obtained from the request.
    """
    try:
        route_id = request.json.get('route_id')
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM data WHERE route_id = ?  AND id = ?", (route_id, id))
        conn.commit()
        return {"status": "success", "message": "Data deleted successfully by id"}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Failed to delete data by id: {e}"}
    finally:
        conn.close()



# Initialize the database when the module is loaded
initialize_db()
