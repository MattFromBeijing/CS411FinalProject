from dataclasses import dataclass
import logging
import os

from workout.utils.sql_utils import get_db_connection
from workout.utils.logger import configure_logger

from datetime import datetime
from exercise_model import Exercise

logger = logging.getLogger(__name__)
configure_logger(logger)

@dataclass
class Log:
    id: int
    user_id: int
    exercise_names: str
    muscle_groups: int
    date: str

def create_log(id: int, user_id: int, username: str, exercise_name: str, muscle_group: int, date: str) -> bool:
    if len(username) < 0:
        raise ValueError(f"Invalid exercise name provided: {username} (must be an string with length greater than 0).")
    if len(title) < 0:
        raise ValueError(f"Invalid exercise name provided: {title} (must be an string with length greater than 0).")
    if len(exercise_name) < 0:
        raise ValueError(f"Invalid exercise name provided: {exercise_name} (must be an string with length greater than 0).")
    if len(date) < 0:
        raise ValueError(f"Invalid exercise name provided: {date} (must be an string with length greater than 0).")

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Invalid date format provided: {date_str} (expected format: YYYY-MM-DD)") from e

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO logs (user_id, username, title, exercise_name, muscle_group, date) VALUES (?, ?, ?, ?, ?, ?)", (user_id, username, title, exercise_name, muscle_group, date))
            conn.commit()
        return True
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")

def clear_logs(user_id: int):
    pass

def get_all_logs(user_id: int):
    pass

def get_log_by_date(user_id: int, date: str):
    pass

def get_logs_by_muscle_group(user_id: int, muscle_group: int):
    pass

def update_log(user_id: int, date: str, exercise_name: str, muscle_groups: int):
    pass