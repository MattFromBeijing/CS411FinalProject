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
    username: str
    exercise_name: str
    muscle_groups: str
    date: str

######################################################
#
#    Creating Logs
#
######################################################

def create_log(username: str, exercise_name: str, muscle_groups: str, date: str) -> bool:
    """
    Creates a new log entry for a user.

    Args:
        username (str): The username of the user.
        exercise_name (str): The name of the exercise performed.
        muscle_groups (str): Comma-separated muscle groups targeted by the exercise.
        date (str): The date of the log entry in the format YYYY-MM-DD.

    Returns:
        bool: True if the log is created successfully.

    Raises:
        ValueError: If the exercise name is empty, the date format is invalid, 
                    or a duplicate log exists for the username and date.
        sqlite3.Error: For any database-related errors.
    """
    if len(exercise_name) == 0:
        raise ValueError("Invalid exercise name provided. exercise_name must be an string with length greater than 0.")

    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Invalid date format provided: {date}. date must be in format: YYYY-MM-DD")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs WHERE username = ? AND date = ?", (username, date,))
            rows = cursor.fetchall()
        if len(rows) > 0:
            raise ValueError(f"Duplicate date={date} for user={username}.")
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO logs (username, exercise_name, muscle_groups, date) VALUES (?, ?, ?, ?)", 
                (username, exercise_name, muscle_groups, date)
            )
            conn.commit()
        return True
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")

######################################################
#
#    Deleting Logs
#
######################################################

def clear_logs(username: str) -> bool:
    """
    Deletes all logs for a specific user.

    Args:
        username (str): The username whose logs should be deleted.

    Returns:
        bool: True if logs are cleared successfully.

    Raises:
        ValueError: If no logs are found for the user.
        sqlite3.Error: For any database-related errors.
    """

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM logs WHERE username = ?", (username,))
            conn.commit()

            if cursor.rowcount == 0:
                raise ValueError(f"No logs found for username={username}")
        return True
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")
    
def delete_log_by_date(username: str, date: str) -> bool:
    """
    Deletes a specific log for a user by date.

    Args:
        username (str): The username of the user.
        date (str): The date of the log entry to delete in the format YYYY-MM-DD.

    Returns:
        bool: True if the log is deleted successfully.

    Raises:
        ValueError: If the date format is invalid or no log is found for the username and date.
        sqlite3.Error: For any database-related errors.
    """
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Invalid date format provided: {date}. date must be in format: YYYY-MM-DD")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM logs WHERE username = ? AND date = ?", (username, date))
            conn.commit()

            if cursor.rowcount == 0:
                raise ValueError(f"No logs found for username={username} and date={date}")
        return True
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")

######################################################
#
#    Getting Logs
#
######################################################

def get_all_logs(username: str) -> List[Log]:
    """
    Retrieves all logs for a specific user.

    Args:
        username (str): The username of the user.

    Returns:
        List[Log]: A list of Log objects representing all logs for the user.

    Raises:
        sqlite3.Error: For any database-related errors.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs WHERE username = ?", (username,))
            rows = cursor.fetchall()
        if rows:
            logs = [Log(row[0], row[1], row[2], row[3], row[4]) for row in rows]
            return logs
        else:
            return []
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")

def get_log_by_date(username: str, date: str) -> Log:
    """
    Retrieves a specific log for a user by date.

    Args:
        username (str): The username of the user.
        date (str): The date of the log entry to retrieve in the format YYYY-MM-DD.

    Returns:
        Log: The Log object for the specified username and date, or None if no log is found.

    Raises:
        ValueError: If the date format is invalid.
        sqlite3.Error: For any database-related errors.
    """
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Invalid date format provided: \'{date}\'. date must be in format: YYYY-MM-DD") from e
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM logs WHERE username = ? AND date = ?",
                (username, date)
            )
            row = cursor.fetchone()
            
        if row:
            return Log(row[0], row[1], row[2], row[3], row[4])
        else:
            return None
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")

def get_logs_by_muscle_group(username: str, muscle_groups: str) -> List[Log]:
    """
    Retrieves logs for a user based on targeted muscle groups.

    Args:
        username (str): The username of the user.
        muscle_groups (str): Comma-separated list of muscle groups to filter logs.

    Returns:
        List[Log]: A list of Log objects matching the specified muscle groups.

    Raises:
        sqlite3.Error: For any database-related errors.
    """
    try:
        # Convert the input string to a list of integers
        muscle_group_list = [group.strip() for group in muscle_groups.split(",") if group.strip()]
        
        if not muscle_group_list:
            return []
        
        # Build the dynamic WHERE clause for `LIKE` matching
        like_clauses = " OR ".join(["muscle_groups LIKE ?"] * len(muscle_group_list))
        query = f"SELECT * FROM logs WHERE username = ? AND ({like_clauses})"
        
        # Prepare parameters: username + %group% for each muscle group
        parameters = [username] + [f"%{group}%" for group in muscle_group_list]

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

def update_log(username: str, date: str, exercise_name: str, muscle_groups: str) -> bool:
    """
    Updates a log entry for a user.

    Args:
        username (str): The username of the user.
        date (str): The date of the log entry to update in the format YYYY-MM-DD.
        exercise_name (str): The updated name of the exercise.
        muscle_groups (str): The updated comma-separated muscle groups targeted by the exercise.

    Returns:
        bool: True if the log is updated successfully.

    Raises:
        ValueError: If the date format is invalid or no log is found for the username and date.
        sqlite3.Error: For any database-related errors.
    """
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Invalid date format provided: \'{date}\'. date must be in format: YYYY-MM-DD") from e

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE logs SET exercise_name = ?, muscle_groups = ? WHERE username = ? AND date = ?",
                (exercise_name, muscle_groups, username, date)
            )
            conn.commit()

            if cursor.rowcount == 0:
                raise ValueError(f"No log found for username={username} and date={date}")
        return True
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {str(e)}")