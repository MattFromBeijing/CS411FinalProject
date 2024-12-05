from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from utils.sql_utils import check_database_connection, get_db_connection, check_table_exists
import sqlite3
import hashlib
import os

# from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# This bypasses standard security stuff we'll talk about later
# If you get errors that use words like cross origin or flight,
# uncomment this
# CORS(app)

def hash_password(password: str, salt: str) -> str:
    """
    Hashes a password using a salt and SHA-256.

    Args:
        password (str): The plaintext password to hash.
        salt (str): The salt to use for hashing.

    Returns:
        str: The resulting hexadecimal hash of the salted password.
    """
    # Combine the salt and the password
    salted_password = salt + password

    # Create a SHA-256 hash of the salted password
    hashed = hashlib.sha256(salted_password.encode()).hexdigest()

    return hashed

####################################################
#
# Healthchecks
#
####################################################

@app.route('/api/health', methods=['GET'])
def healthcheck() -> Response:
    """
    Health check route to verify the service is running.

    Returns:
        JSON response indicating the health status of the service.
    """
    app.logger.info('Health check')
    return make_response(jsonify({'status': 'healthy'}), 200)



@app.route('/api/create-account', methods=['POST'])
def create_account() -> Response:
    """
    Route to create a new user account.

    Expected JSON Input:
        - username (str): The user's chosen username.
        - password (str): The user's chosen password.

    Returns:
        JSON response indicating success or failure.
    Raises:
        400 error if input validation fails.
        500 error if there is an issue creating the account in the database.
    """
    app.logger.info("Creating a new account")
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            app.logger.error("Invalid input: Username and password are required")
            return make_response(jsonify({'error': 'Username and password are required'}), 400)

        salt = os.urandom(16).hex()
        hashed_password = hash_password(password, salt)

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO login (username, salt, hashed_password) VALUES (?, ?, ?)',
            (username, salt, hashed_password)
        )
        conn.commit()
        conn.close()
        app.logger.info("Account created successfully for username: %s", username)
        return make_response(jsonify({'message': 'Account created successfully'}), 201)
    except sqlite3.IntegrityError:
        app.logger.error("Username already exists: %s", username)
        return make_response(jsonify({'error': 'Username already exists'}), 400)
    except Exception as e:
        app.logger.error("Error creating account: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/api/login', methods=['POST'])
def login() -> Response:
    """
    Route to log in a user.

    Expected JSON Input:
        - username (str): The user's username.
        - password (str): The user's password.

    Returns:
        JSON response indicating success or failure.
    Raises:
        400 error if credentials are invalid.
    """
    app.logger.info("User login attempt")
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            app.logger.error("Invalid input: Username and password are required")
            return make_response(jsonify({'error': 'Username and password are required'}), 400)

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM login WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user is None:
            app.logger.warning("Invalid login attempt: User not found")
            return make_response(jsonify({'error': 'Invalid username or password'}), 400)

        salt = user['salt']
        stored_hashed_password = user['hashed_password']
        if hash_password(password, salt) == stored_hashed_password:
            app.logger.info("Login successful for username: %s", username)
            return make_response(jsonify({'message': 'Login successful'}), 200)
        else:
            app.logger.warning("Invalid login attempt: Incorrect password")
            return make_response(jsonify({'error': 'Invalid username or password'}), 400)
    except Exception as e:
        app.logger.error("Error during login: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/api/update-password', methods=['POST'])
def update_password() -> Response:
    """
    Route to update a user's password.

    Expected JSON Input:
        - username (str): The user's username.
        - old_password (str): The user's current password.
        - new_password (str): The user's new password.

    Returns:
        JSON response indicating success or failure.
    Raises:
        400 error if input validation fails or old password is incorrect.
    """
    app.logger.info("Password update attempt")
    try:
        data = request.get_json()
        username = data.get('username')
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not username or not old_password or not new_password:
            app.logger.error("Invalid input: All fields are required")
            return make_response(jsonify({'error': 'All fields are required'}), 400)

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM login WHERE username = ?', (username,)).fetchone()

        if user is None:
            app.logger.warning("User not found during password update: %s", username)
            conn.close()
            return make_response(jsonify({'error': 'User does not exist'}), 400)

        salt = user['salt']
        stored_hashed_password = user['hashed_password']
        if hash_password(old_password, salt) != stored_hashed_password:
            app.logger.warning("Old password incorrect for username: %s", username)
            conn.close()
            return make_response(jsonify({'error': 'Old password is incorrect'}), 400)

        new_salt = os.urandom(16).hex()
        new_hashed_password = hash_password(new_password, new_salt)

        conn.execute(
            'UPDATE login SET salt = ?, hashed_password = ?, updated_at = CURRENT_TIMESTAMP WHERE username = ?',
            (new_salt, new_hashed_password, username)
        )
        conn.commit()
        conn.close()
        app.logger.info("Password updated successfully for username: %s", username)
        return make_response(jsonify({'message': 'Password updated successfully'}), 200)
    except Exception as e:
        app.logger.error("Error updating password: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)
