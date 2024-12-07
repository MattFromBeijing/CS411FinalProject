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
    Log into a user stored in the users table.

    Args:
        username (str): The user's username.
        password (str): The password for the user.

        Raises:
            ValueError: If a user with the username already exists.
        """
        salt, hashed_password = self._generate_hashed_password(password)
        new_user = self(username=username, salt=salt, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            logger.info("User successfully added to the database: %s", username)
        except IntegrityError:
            db.session.rollback()
            logger.error("Duplicate username: %s", username)
            raise ValueError(f"User with username '{username}' already exists")
        except Exception as e:
            db.session.rollback()
            logger.error("Database error: %s", str(e))
            raise

    def check_password(self, username: str, password: str) -> bool:
        """
        Check if a given password matches the stored password for a user.

        Args:
            username (str): The username of the user.
            password (str): The password to check.

        Returns:
            bool: True if the password is correct, False otherwise.

        Raises:
            ValueError: If the user does not exist.
        """
        user = self.query.filter_by(username=username).first()
        if not user:
            logger.info("User %s not found", username)
            raise ValueError(f"User {username} not found")
        hashed_password = hashlib.sha256((password + user.salt).encode()).hexdigest()
        return hashed_password == user.password

    def delete_user(self, username: str) -> None:
        """
        Delete a user from the database.

        Args:
            username (str): The username of the user to delete.

        Raises:
            ValueError: If the user does not exist.
        """
        user = self.query.filter_by(username=username).first()
        if not user:
            logger.info("User %s not found", username)
            raise ValueError(f"User {username} not found")
        db.session.delete(user)
        db.session.commit()
        logger.info("User %s deleted successfully", username)

    def get_id_by_username(self, username: str) -> int:
        """
        Retrieve the ID of a user by username.

        Args:
            username (str): The username of the user.

        Returns:
            int: The ID of the user.

        Raises:
            ValueError: If the user does not exist.
        """
        user = self.query.filter_by(username=username).first()
        if not user:
            logger.info("User %s not found", username)
            raise ValueError(f"User {username} not found")
        return user.id

    @classmethod
    def update_password(self, username: str, new_password: str) -> None:
        """
        Update the password for a user.

        Args:
            username (str): The username of the user.
            new_password (str): The new password to set.

    Raises:
        sqlite3.Error: If any database error occurs.
    """
    try:
        with open(os.getenv("SQL_CREATE_TABLE_PATH", "/app/sql/create_tables.sql"), "r") as fh:
            create_table_script = fh.read()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(create_table_script)
            conn.commit()

            logger.info("Users cleared successfully.")
    except sqlite3.Error as e:
        logger.error("Database error while clearing catalog: %s", str(e))
        raise e
