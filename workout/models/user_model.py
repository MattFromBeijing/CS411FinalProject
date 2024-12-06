import hashlib
import logging
import os
import sqlite3

from workout.db import db
from workout.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

class User:

    id = int
    username = str
    salt = str
    password = str

    def _generate_hashed_password(self, password: str) -> tuple[str, str]:
        """
        Generates a salted, hashed password.

        Args:
            password (str): The password to hash.

        Returns:
            tuple: A tuple containing the salt and hashed password.
        """
        salt = os.urandom(16).hex()
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        return salt, hashed_password

    def create_user(self, username: str, password: str) -> None:
        """
        Create a new user with a salted, hashed password.

        Args:
            username (str): The username of the user.
            password (str): The password to hash and store.

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
            ValueError: If the user does not exist.
        """
        user = self.query.filter_by(username=username).first()
        if not user:
            logger.info("User %s not found", username)
            raise ValueError(f"User {username} not found")

        salt, hashed_password = self._generate_hashed_password(new_password)
        user.salt = salt
        user.password = hashed_password
        db.session.commit()
        logger.info("Password updated successfully for user: %s", username)