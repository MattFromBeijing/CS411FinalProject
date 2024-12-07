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
    muscle_groups: str
    date: str

def create_log(id: int, user_id: int, exercise_name: str, muscle_groups: str, date: str) -> bool:
    if len(exercise_name) < 0:
        raise ValueError(f"Invalid exercise name provided: [empty str] (must be an string with length greater than 0).")

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Invalid date format provided: {date_str} (expected format: YYYY-MM-DD)") from e

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO logs (user_id, exercise_name, muscle_groups, date) VALUES (?, ?, ?, ?)", 
                (user_id, exercise_name, muscle_groups, date)
            )
            conn.commit()
        return True
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")

def clear_logs(user_id: int) -> bool:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM logs WHERE user_id = ?", (user_id))
            conn.commit()

            if cursor.rowcount == 0:
                raise ValueError(f"No logs found for user_id={user_id}")
        return True
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")

def get_all_logs(user_id: int) -> List[Log]:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs WHERE user_id = ?", (user_id,))
            rows = cursor.fetchall()
        logs = [Log(id=row[0], user_id=row[1], exercise_name=row[2], muscle_groups=row[3], date=row[4]) for row in rows]
        return logs
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")

def get_log_by_date(user_id: int, date: str) -> Log:
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Invalid date format provided: {date_str} (expected format: YYYY-MM-DD)") from e
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, user_id, exercise_name, muscle_groups, date FROM logs WHERE user_id = ? AND date = ?",
                (user_id, date)
            )
            row = cursor.fetchone()
            
        if row:
            return Log(id=row[0], user_id=row[1], exercise_name=row[2], muscle_groups=row[3], date=row[4])
        else:
            raise ValueError(f"No log found for user_id={user_id} and date={date}")
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")

def get_logs_by_muscle_group(user_id: int, muscle_groups: str) -> List[Log]:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, user_id, exercise_name, muscle_group, date FROM logs WHERE user_id = ? AND muscle_groups = ?",
                (user_id, muscle_groups)
            )
            rows = cursor.fetchall()
        
        if row:
            logs = [Log(id=row[0], user_id=row[1], exercise_name=row[2], muscle_group=row[3], date=row[4]) for row in rows]
            return logs
        else:
            raise ValueError(f"No log found for user_id={user_id} and muscle_groups={date}")
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")


def update_log(user_id: int, date: str, exercise_name: str, muscle_groups: str) -> bool:
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Invalid date format provided: {date_str} (expected format: YYYY-MM-DD)") from e

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE logs SET exercise_name = ?, muscle_groups = ? WHERE user_id = ? AND date = ?",
                (exercise_name, muscle_groups, user_id, date)
            )
            conn.commit()

            if cursor.rowcount == 0:
                raise ValueError(f"No log found for user_id={user_id} and date={date}")
        return True
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")