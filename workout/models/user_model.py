from dataclasses import dataclass
import logging
import os
import sqlite3
import hashlib
from workout.utils.logger import configure_logger
from workout.utils.sql_utils import get_db_connection

logger = logging.getLogger(__name__)
configure_logger(logger)

@dataclass
class User:
    id: int
    username: str
    salt: str
    hashed_password: str


def hash_password(password: str, salt: bytes) -> str:
    """
    Hashes a password with the given salt using SHA-256.

    Args:
        password (str): The password to hash.
        salt (bytes): The salt to use.

    Returns:
        str: The hexadecimal representation of the hashed password.
    """
    return hashlib.sha256(password.encode('utf-8') + salt).hexdigest()


def login(username: str, password: str) -> bool:
    """
    Log into a user stored in the login table.

    Args:
        username (str): The user's username.
        password (str): The password for the user.

    Raises:
        ValueError: If the username is invalid.
        sqlite3.Error: For any other database errors.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            logger.info("Attempting to login user with username %s", username)

            cursor.execute("SELECT salt, hashed_password FROM login WHERE username = ?", (username,))
            row = cursor.fetchone()

            if row:
                salt, hashed_password = row[0], row[1]
                # Check the password
                if hashed_password == hash_password(password, bytes.fromhex(salt)):
                    logger.info("Logged into user with username %s", username)
                    return True
                else:
                    logger.info("Incorrect password for user with username %s", username)
                    return False
            else:
                logger.info("User with username %s not found", username)
                raise ValueError(f"User with username {username} not found")
    except sqlite3.Error as e:
        logger.error("Database error while logging in user with username %s: %s", username, str(e))
        raise e


def create_user(username: str, password: str) -> None:
    """
    Creates a new user in the login table.

    Args:
        username (str): The user's username.
        password (str): The password for the user.

    Raises:
        ValueError: If username is invalid.
        sqlite3.IntegrityError: If a user with the same username already exists.
        sqlite3.Error: For any other database errors.
    """
    salt = os.urandom(16)
    hashed_password = hash_password(password, salt)
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO login (username, salt, hashed_password)
                VALUES (?, ?, ?)
            """, (username, salt.hex(), hashed_password))
            conn.commit()

            logger.info("User created successfully: %s", username)
    except sqlite3.IntegrityError as e:
        logger.error("User with username '%s' already exists.", username)
        raise ValueError(f"User with username '{username}' already exists.") from e
    except sqlite3.Error as e:
        logger.error("Database error while creating user: %s", str(e))
        raise sqlite3.Error(f"Database error: {str(e)}")


def update_password(username: str, password: str) -> None:
    """
    Updates a user's password.

    Args:
        username (str): The username for the user to update.
        password (str): The new password for the user.

    Raises:
        ValueError: If the user does not exist.
        sqlite3.Error: If there is a database error.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            logger.info("Attempting to update password for user with username %s", username)

            cursor.execute("SELECT salt FROM login WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                salt = row[0]
                hashed_password = hash_password(password, bytes.fromhex(salt))
                cursor.execute("UPDATE login SET hashed_password = ? WHERE username = ?", (hashed_password, username))
                conn.commit()

                logger.info("Password updated for user with username: %s", username)
            else:
                logger.info("User with username %s not found", username)
                raise ValueError(f"User with username {username} not found")
    except sqlite3.Error as e:
        logger.error("Database error while updating password for user with username %s: %s", username, str(e))
        raise e

def clear_users() -> None:
    """
    Recreates the login table, effectively deleting all users.

    Raises:
        sqlite3.Error: If any database error occurs.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript("""
                DROP TABLE IF EXISTS login;
                CREATE TABLE login (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    salt TEXT NOT NULL,
                    hashed_password TEXT NOT NULL
                );
            """)
            conn.commit()

            logger.info("Users cleared successfully.")
    except sqlite3.Error as e:
        logger.error("Database error while clearing login table: %s", str(e))
        raise e

def get_id_by_username(username: str) -> int:
    """
    Retrieves the ID of a user by their username.

    Args:
        username (str): The username of the user.

    Returns:
        int: The ID of the user.

    Raises:
        ValueError: If the user is not found.
        sqlite3.Error: If there is a database error.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            logger.info("Retrieving user ID for username %s", username)

            cursor.execute("SELECT id FROM login WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                raise ValueError(f"User with username {username} not found")
    except sqlite3.Error as e:
        logger.error("Database error while retrieving user ID for username %s: %s", username, str(e))
        raise e
