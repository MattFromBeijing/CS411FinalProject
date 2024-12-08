from dataclasses import dataclass
import logging
import os
import sqlite3

from workout.utils.sql_utils import get_db_connection
from workout.utils.logger import configure_logger

from typing import List
from datetime import datetime

logger = logging.getLogger(__name__)
configure_logger(logger)

@dataclass
class Log:
    id: int
    user_id: int
    exercise_name: str
    muscle_groups: str
    date: str

def create_log(user_id: int, exercise_name: str, muscle_groups: str, date: str) -> bool:
    if len(exercise_name) == 0:
        raise ValueError("Invalid exercise name provided. exercise_name must be an string with length greater than 0.")

    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Invalid date format provided: {date}. date must be in format: YYYY-MM-DD")

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
        if rows:
            logs = [Log(row[0], row[1], row[2], row[3], row[4]) for row in rows]
            return logs
        else:
            return []
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")

def get_log_by_date(user_id: int, date: str) -> Log:
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Invalid date format provided: \'{date}\'. date must be in format: YYYY-MM-DD") from e
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM logs WHERE user_id = ? AND date = ?",
                (user_id, date)
            )
            row = cursor.fetchone()
            
        if row:
            return Log(row[0], row[1], row[2], row[3], row[4])
        else:
            return None
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")

def get_logs_by_muscle_group(user_id: int, muscle_groups: str) -> List[Log]:
    try:
        # Convert the input string to a list of integers
        muscle_group_list = [group.strip() for group in muscle_groups.split(",") if group.strip().isdigit()]
        
        if not muscle_group_list:
            return []
        
        # Build the dynamic WHERE clause for `LIKE` matching
        like_clauses = " OR ".join(["muscle_groups LIKE ?"] * len(muscle_group_list))
        query = f"SELECT * FROM logs WHERE user_id = ? AND ({like_clauses})"
        
        # Prepare parameters: user_id + %group% for each muscle group
        parameters = [user_id] + [f"%{group}%" for group in muscle_group_list]

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            rows = cursor.fetchall()

        if rows:
            logs = [Log(row[0], row[1], row[2], row[3], row[4]) for row in rows]
            return logs
        else:
            return []

    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")


def update_log(user_id: int, date: str, exercise_name: str, muscle_groups: str) -> bool:
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Invalid date format provided: \'{date}\'. date must be in format: YYYY-MM-DD") from e

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