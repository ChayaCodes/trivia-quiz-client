import time
import requests
from flask import request
import json
from difflib import SequenceMatcher
from datetime import datetime, timedelta



class TemporaryRequest:
    def __init__(self, request):
        self.json = request.json  # מעתיק את json מתוך request המקורי


def get_analysis_response(analysis_response_url=None):
    """
    Retrieves and validates the response from 'analysis_response_url' in the request.
    If 'analysis_response_url' is missing, returns an error message.
    If the response is not a valid JSON/dictionary or convertible string, returns None.

    :return: Parsed JSON/dictionary if valid; None if response is not in a valid format.
    """
    
    
    if analysis_response_url is None:
        analysis_response_url = request.json.get('analysis_response_url')
    if not analysis_response_url:
        return None
        # return {"status": "error", "message": "Missing 'analysis_response_url' in request"}

    try:
        # Make a request to the URL
        response = requests.get(analysis_response_url)
        # Attempt to parse the response as JSON or dictionary
        data = response.json() if response.headers.get('Content-Type') == 'application/json' else None
        if isinstance(data, dict):
            return data

        # If response is a string, attempt to parse as JSON
        if isinstance(response.text, str):
            data = json.loads(response.text)
            if isinstance(data, dict):
                return data

        # If not valid JSON or dictionary, return None
        return None

    except (requests.RequestException, ValueError, json.JSONDecodeError):
        # Return None if there's a request error or JSON parsing fails
        return None

def wait_for_analysis_response(analysis_response_url=None, retries=10, wait_time=1):
    """
    Waits for a valid response from 'analysis_response_url'. Retries if the response is invalid.

    :param retries: Number of retry attempts.
    :param wait_time: Time (in seconds) to wait between retries.
    :return: Parsed JSON/dictionary if valid; None if maximum retries reached without valid response.
    """
    if analysis_response_url is None:
        analysis_response_url = request.json.get('analysis_response_url')
    if not analysis_response_url:
        return None
      
    for attempt in range(retries):
        response = get_analysis_response(analysis_response_url)
        if response is not None:
            return response
        # Wait before the next attempt
        time.sleep(wait_time)

    # Return None if all retries fail
    return None

def get_similarity_rate(value1, value2):
    """
    Calculate the similarity rate between two string values.

    The function calculates the similarity ratio between `value1` and `value2` 
    using the `SequenceMatcher` from the `difflib` library. If one of the values
    is a substring of the other (but they are not exactly the same), the function 
    overrides the similarity rate to 0.9.

    Parameters:
        value1 (str): The first string to compare.
        value2 (str): The second string to compare.

    Returns:
        float: A similarity rate between 0 and 1, where 1 indicates a perfect match.
            If one string is a substring of the other, the rate will be set to 0.9.
    """
    
    similarity = SequenceMatcher(None, value1, value2).ratio()
        
        # אם target_value מופיע בתוך topic, קובע את הדמיון ל-0.9
    if value1 != value2 and (value1 in value2 or value2 in value1)  :
        similarity = 0.9
            
    return similarity




def get_similarity_results(data, target_value, similarity_threshold=0.6):
    """
    מחשבת את הדמיון בין ערך יעד למחרוזות בתוך רשימת מילונים ומחזירה רשימה ממוינת של תוצאות.

    פרמטרים:
    ----------
    data : list of dict
        רשימה של מילונים, כאשר כל מילון מכיל מפתח אחד בלבד - 'ID' וערך טקסטואלי תחת המפתח הזה.
        לדוגמה: [{"1": "גמרא בבא מציאה"}, {"2": "גמרא בבא בתרא"}]

    target_value : str
        המחרוזת איתה נשווה את ערכי הטקסט ברשימת הנתונים כדי לחשב את אחוזי הדמיון.

    similarity_threshold : float, אופציונלי (ברירת מחדל היא 0.6)
        הסף המינימלי של אחוז הדמיון הנדרש להוספת התוצאה לרשימה.
        אם `target_value` נמצא בתוך מחרוזת אחרת, הדמיון יקבע ל-0.9 גם אם הוא נמוך מהסף.

    החזרה:
    -------
    list of dict
        רשימה ממוינת של מילונים, כאשר כל מילון מכיל את המפתחות הבאים:
        - 'id': מחרוזת המייצגת את ה-ID מתוך הנתונים המקוריים
        - 'topic': מחרוזת המתארת את הטקסט המתאים מתוך הנתונים
        - 'similarity': ערך הדמיון בין `target_value` לבין `topic` (float)

    דוגמה לשימוש:
    -------------
    >>> data = [
            {"1": "גמרא בבא מציאה"},
            {"2": "גמרא בבא בתרא"},
            {"3": "גמרא"},
            {"4": "בבא מציאה"},
        ]
    >>> target_value = "גמרא"
    >>> get_similarity_results(data, target_value)
    [
        {'id': '3', 'topic': 'גמרא', 'similarity': 1.0},
        {'id': '1', 'topic': 'גמרא בבא מציאה', 'similarity': 0.9},
        {'id': '2', 'topic': 'גמרא בבא בתרא', 'similarity': 0.9}
    ]
    """
    results = []
    for item in data:
        topic = list(item.values())[0]
        id = list(item.keys())[0]
        
        # # חישוב הדמיון
        # similarity = SequenceMatcher(None, topic, target_value).ratio()
        
        # # אם target_value מופיע בתוך topic, קובע את הדמיון ל-0.9
        # if target_value != topic and (target_value in topic or topic in target_value)  :
        #     similarity = 0.9
        similarity=get_similarity_rate(target_value, topic)
        # הוספת התוצאה לרשימה אם הדמיון גבוה מספיק או שה-target_value נמצא במחרוזת
        if similarity >= similarity_threshold:
            results.append({"id": id, "topic": topic, "similarity": similarity})
    
    # מיון הרשימה לפי ערך הדמיון בסדר יורד
    sorted_results = sorted(results, key=lambda x: x["similarity"], reverse=True)
    
    return sorted_results



def get_next_item(data_list, key=None):
    """
    Retrieve the next item in a list based on a given key, or the first item if no key is provided.

    This function iterates over `data_list` to find the position of the first item containing the specified `key`.
    If the key is found, it returns the item immediately following it. If the key is not found or there is no
    following item, it returns the first item in the list. If `key` is not provided, it simply returns the first item.

    Parameters:
        data_list (list): A list of dictionaries or objects to search through.
        key (str, optional): The key to search for in each item of `data_list`. If not provided, 
                             the function returns the first item in the list.

    Returns:
        dict or object or None: The item immediately after the item containing `key`, or the first item if `key` is not found. 
                                If `data_list` is empty, it returns None.

    Examples:
        >>> data_list = [{"id": 1}, {"id": 2}, {"id": 3}]
        >>> get_next_item(data_list, "id")    # Returns the second item
        {'id': 2}
        
        >>> get_next_item(data_list, "id", 3) # Returns None as there is no item after `id` 3
        None
        
        >>> get_next_item(data_list)          # Returns the first item
        {'id': 1}
        
        >>> get_next_item([], "id")           # Returns None as the list is empty
        None
    """
    # אם לא נתקבל מפתח, מחזיר את הפריט הראשון
    if key is None:
        return data_list[0] if data_list else None
    
    # חיפוש המיקום של הפריט עם המפתח הנתון
    for i, item in enumerate(data_list):
        if key in item:
            # אם יש פריט הבא, מחזיר אותו
            return data_list[i + 1] if i + 1 < len(data_list) else None
    
    # אם המפתח לא נמצא, מחזיר את הפריט הראשון
    return data_list[0] if data_list else None



def normalize_phone_number(phone_number):
    """
    Normalize an Israeli phone number by replacing the country code prefix with a '0'.

    This function checks if the input `phone_number` starts with '972' or '+972',
    indicating an Israeli country code. If so, it replaces the country code with '0' 
    to format the number in the local style. If the number does not start with these
    prefixes, it is returned as-is.

    Parameters:
        phone_number (str): The phone number to be normalized.

    Returns:
        str: The normalized phone number with the country code replaced by '0', 
             or the original phone number if no replacement was needed.

    Examples:
        >>> normalize_phone_number("972501234567")
        '0501234567'
        >>> normalize_phone_number("+972501234567")
        '0501234567'
        >>> normalize_phone_number("0501234567")
        '0501234567'
    """
    if phone_number.startswith("972"):
        return "0" + phone_number[3:]
    elif phone_number.startswith("+972"):
        return "0" + phone_number[4:]
    return phone_number



def time_code_to_unix(day_of_week: str, time: str) -> int:
    """
    ממיר יום ושעה נתונים לפורמט זמן יוניקס (שניות מאז 1 בינואר 1970).

    Parameters:
        day_of_week (str): מחרוזת המייצגת את היום בשבוע. ערכים אפשריים:
                          - "0" מתייחס ליום הנוכחי.
                          - "1" עד "7" מתייחסים ליום ראשון עד שבת בהתאמה.
        time (str): מחרוזת המייצגת את השעה והדקה בפורמט "HHMM".
                    לדוגמה: "1730" עבור 17:30.

    Returns:
        int: חותמת זמן יוניקס המייצגת את היום והשעה המבוקשים.
    
    Examples:
        >>> time_code_to_unix("0", "1730")
        1735342200  # (תלוי ביום הנוכחי)

        >>> time_code_to_unix("3", "0800")
        1735504800  # (יום שלישי הקרוב בשעה 08:00)
    """
    now = datetime.now()
    current_weekday = (now.weekday() + 1) % 7 + 1  # התאמה כך שיום ראשון = 1

    # המרה מ-str ל-int
    day_of_week = int(day_of_week) or current_weekday
    hours = int(time[:2])  # שתי הספרות הראשונות = שעה
    minutes = int(time[2:])  # שתי הספרות האחרונות = דקות

    # היום הנוכחי
    
    # חישוב הפרש הימים
    days_difference = (day_of_week - current_weekday) % 7

    # יצירת תאריך היעד
    target_date = now + timedelta(days=days_difference)
    target_datetime = target_date.replace(hour=hours, minute=minutes, second=0, microsecond=0)

    # המרה ליוניקס טיים
    unix_time = int(target_datetime.timestamp())
    return unix_time

