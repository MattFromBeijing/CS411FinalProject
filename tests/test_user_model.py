import pytest
import sqlite3
import os
import hashlib
from workout.models.user_model import create_user, hash_password, login, update_password, clear_users, get_db_connection

# SQLite schema for testing
CREATE_LOGIN_TABLE = """
CREATE TABLE IF NOT EXISTS login (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    salt TEXT NOT NULL,
    hashed_password TEXT NOT NULL
);
"""

@pytest.fixture
def test_db():
    """Fixture to set up a temporary database for testing."""
    db_path = "test_login.db"
    conn = sqlite3.connect(db_path)
    conn.executescript(CREATE_LOGIN_TABLE)
    conn.commit()

    yield db_path  # Provide the database path to the tests

    conn.close()
    os.remove(db_path)  # Clean up after the test

@pytest.fixture
def mock_get_db_connection(test_db, monkeypatch):
    """Fixture to mock the `get_db_connection` function."""
    def mock_connection():
        return sqlite3.connect(test_db)

    monkeypatch.setattr("workout.models.user_model.get_db_connection", mock_connection)

@pytest.fixture
def sample_user():
    """Provide a sample user for testing."""
    return {
        "username": "testuser",
        "password": "securepassword123"
    }

##########################################################
# Hash Password
##########################################################

def test_hash_password():
    """
    Test the hash_password function with a sample password and salt.
    """
    password = "mypassword"
    salt = b"randomsalt"
    expected_hash = hashlib.sha256(password.encode('utf-8') + salt).hexdigest()

    # Assert the function output matches the expected hash
    assert hash_password(password, salt) == expected_hash, "The hash does not match the expected value."

##########################################################
# User Creation
##########################################################

def test_create_account(mock_get_db_connection, sample_user):
    """Test creating a new user with a unique username."""
    from workout.models.user_model import get_db_connection
    #This is weird as fuck but I need this for some stupid reason
    create_user(sample_user["username"], sample_user["password"])

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, salt, hashed_password FROM login WHERE username = ?", (sample_user["username"],))
        user = cursor.fetchone()

    assert user is not None, "User should be created in the database."
    assert user[0] == sample_user["username"], "Username should match the input."
    assert len(user[1]) == 32, "Salt should be 32 characters (hex)."
    assert len(user[2]) == 64, "Password should be a 64-character SHA-256 hash."

def test_create_duplicate_user(mock_get_db_connection, sample_user):
    """Test attempting to create a user with a duplicate username."""
    create_user(sample_user["username"], sample_user["password"])
    with pytest.raises(ValueError, match="User with username 'testuser' already exists"):
        create_user(sample_user["username"], sample_user["password"])

##########################################################
# User Authentication
##########################################################

def test_check_password_correct(mock_get_db_connection, sample_user):
    """Test checking the correct password."""
    create_user(sample_user["username"], sample_user["password"])
    assert login(sample_user["username"], sample_user["password"]) is True, "Password should match."

def test_check_password_incorrect(mock_get_db_connection, sample_user):
    """Test checking an incorrect password."""
    create_user(sample_user["username"], sample_user["password"])
    assert login(sample_user["username"], "wrongpassword") is False, "Password should not match."

def test_check_password_user_not_found(mock_get_db_connection):
    """Test checking password for a non-existent user."""
    with pytest.raises(ValueError, match="User with username nonexistentuser not found"):
        login("nonexistentuser", "password")

##########################################################
# Update Password
##########################################################

def test_update_password(mock_get_db_connection, sample_user):
    """Test updating the password for an existing user."""
    create_user(sample_user["username"], sample_user["password"])
    new_password = "newpassword456"
    update_password(sample_user["username"], new_password)
    assert login(sample_user["username"], new_password) is True, "Password should be updated successfully."

def test_update_password_user_not_found(mock_get_db_connection):
    """Test updating the password for a non-existent user."""
    with pytest.raises(ValueError, match="User with username nonexistentuser not found"):
        update_password("nonexistentuser", "newpassword")

##########################################################
# Clear Users
##########################################################

def test_clear_users(mock_get_db_connection, sample_user):
    """Test clearing all users."""
    create_user(sample_user["username"], sample_user["password"])
    clear_users()

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login WHERE username = ?", (sample_user["username"],))
        user = cursor.fetchone()

    assert user is None, "User should be deleted from the database."

##########################################################
# Get User ID by Username
##########################################################

def test_get_id_by_username(mock_get_db_connection, sample_user):
    """
    Test successfully retrieving a user's ID by their username.
    """
    from workout.models.user_model import get_id_by_username

    # Create a user in the database
    create_user(sample_user["username"], sample_user["password"])

    # Retrieve the user ID
    user_id = get_id_by_username(sample_user["username"])

    # Assert the user ID is valid
    assert user_id > 0, "Retrieved ID should be a valid positive integer."


def test_get_id_by_username_user_not_found(mock_get_db_connection):
    """
    Test failure when retrieving a non-existent user's ID by their username.
    """
    from workout.models.user_model import get_id_by_username

    with pytest.raises(ValueError, match="User with username nonexistentuser not found"):
        get_id_by_username("nonexistentuser")

