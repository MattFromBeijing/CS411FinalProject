import pytest
import sqlite3
import os
from workout.models.user_model import Users, get_db_connection

# SQLite schema for testing
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    salt TEXT NOT NULL,
    hashed_password TEXT NOT NULL
);
"""

@pytest.fixture
def test_db():
    """Fixture to set up a temporary database for testing."""
    db_path = "test_users.db"
    conn = sqlite3.connect(db_path)
    conn.executescript(CREATE_USERS_TABLE)
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
# User Creation
##########################################################

def test_create_account(mock_get_db_connection, sample_user):
    """Test creating a new user with a unique username."""
    Users.create_user(sample_user["username"], sample_user["password"])

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, salt, hashed_password FROM Users WHERE username = ?", (sample_user["username"],))
        user = cursor.fetchone()

    assert user is not None, "User should be created in the database."
    assert user[0] == sample_user["username"], "Username should match the input."
    assert len(user[1]) == 32, "Salt should be 32 characters (hex)."
    assert len(user[2]) == 64, "Password should be a 64-character SHA-256 hash."


def test_create_duplicate_user(mock_get_db_connection, sample_user):
    """Test attempting to create a user with a duplicate username."""
    Users.create_user(sample_user["username"], sample_user["password"])
    with pytest.raises(ValueError, match="User with username 'testuser' already exists"):
        Users.create_user(sample_user["username"], sample_user["password"])


##########################################################
# User Authentication
##########################################################

def test_check_password_correct(mock_get_db_connection, sample_user):
    """Test checking the correct password."""
    Users.create_user(sample_user["username"], sample_user["password"])
    assert Users.login(sample_user["username"], sample_user["password"]) is True, "Password should match."


def test_check_password_incorrect(mock_get_db_connection, sample_user):
    """Test checking an incorrect password."""
    Users.create_user(sample_user["username"], sample_user["password"])
    assert Users.login(sample_user["username"], "wrongpassword") is False, "Password should not match."


def test_check_password_user_not_found(mock_get_db_connection):
    """Test checking password for a non-existent user."""
    with pytest.raises(ValueError, match="User with username nonexistentuser not found"):
        Users.login("nonexistentuser", "password")


##########################################################
# Update Password
##########################################################

def test_update_password(mock_get_db_connection, sample_user):
    """Test updating the password for an existing user."""
    Users.create_user(sample_user["username"], sample_user["password"])
    new_password = "newpassword456"
    Users.update_password(sample_user["username"], new_password)
    assert Users.login(sample_user["username"], new_password) is True, "Password should be updated successfully."


def test_update_password_user_not_found(mock_get_db_connection):
    """Test updating the password for a non-existent user."""
    with pytest.raises(ValueError, match="User with username nonexistentuser not found"):
        Users.update_password("nonexistentuser", "newpassword")


##########################################################
# Delete User
##########################################################

def test_delete_user(mock_get_db_connection, sample_user):
    """Test deleting an existing user."""
    Users.create_user(sample_user["username"], sample_user["password"])
    Users.clear_users()

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", (sample_user["username"],))
        user = cursor.fetchone()

    assert user is None, "User should be deleted from the database."


def test_delete_user_not_found(mock_get_db_connection):
    """Test deleting a non-existent user."""
    with pytest.raises(ValueError, match="User with username nonexistentuser not found"):
        Users.delete_user("nonexistentuser")


##########################################################
# Get User
##########################################################

def test_get_id_by_username(mock_get_db_connection, sample_user):
    """
    Test successfully retrieving a user's ID by their username.
    """
    # Create a user in the database
    Users.create_user(sample_user["username"], sample_user["password"])

    # Retrieve the user ID
    user_id = Users.get_id_by_username(sample_user["username"])

    # Verify the ID is correct
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Users WHERE username = ?", (sample_user["username"],))
        user = cursor.fetchone()

    assert user is not None, "User should exist in the database."
    assert user[0] == user_id, "Retrieved ID should match the user's ID."


def test_get_id_by_username_user_not_found(mock_get_db_connection):
    """
    Test failure when retrieving a non-existent user's ID by their username.
    """
    with pytest.raises(ValueError, match="User with username nonexistentuser not found"):
        Users.get_id_by_username("nonexistentuser")
