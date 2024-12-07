import pytest
import sqlite3
import os

from workout.models.log_model import (
    Log,
    create_log,
    clear_logs,
    get_all_logs,
    get_log_by_date,
    get_logs_by_muscle_group,
    update_log,
)

######################################################
#
#    Fixtures
#
######################################################

def normalize_whitespace(sql_query: str) -> str:
    return re.sub(r'\s+', ' ', sql_query).strip()

# Mocking the database connection for tests
@pytest.fixture
def mock_cursor(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()

    # Mock the connection's cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  # Default return for queries
    mock_cursor.fetchall.return_value = []
    mock_conn.commit.return_value = None

    # Mock the get_db_connection context manager from sql_utils
    @contextmanager
    def mock_get_db_connection():
        yield mock_conn  # Yield the mocked connection object

    mocker.patch("music_collection.models.song_model.get_db_connection", mock_get_db_connection)

    return mock_cursor  # Return the mock cursor so we can set expectations per test

######################################################
#
#    Creating logs
#
######################################################

def test_create_log(mock_cursor):
    """Test creating a new log entry in the database."""

    # Call the function to create a log
    create_log(id=1, user_id=123, exercise_name="Bench Press", muscle_groups="1, 2", date="2024-12-01")

    # Define the expected SQL query
    expected_query = normalize_whitespace("""
        INSERT INTO logs (user_id, exercise_name, muscle_groups, date) 
        VALUES (?, ?, ?, ?)
    """)

    # Capture the actual SQL query executed
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])

    # Assert that the SQL query matches the expected query
    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    # Extract the arguments used in the SQL call
    actual_arguments = mock_cursor.execute.call_args[0][1]

    # Define the expected arguments used in the query
    expected_arguments = (user_id, exercise_name, muscle_groups, date)

    # Assert that the SQL query was executed with the correct arguments
    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}."

def test_create_log_invalid_exercise_name():
    with pytest.raises(ValueError, match="Invalid exercise name provided: [empty str] (must be an string with length greater than 0)."):
        create_log(id=1, user_id=123, exercise_name="", muscle_groups="1, 2", date="2024-12-01")

######################################################
#
#    Deleting logs
#
######################################################

def test_clear_logs():
    pass

def test_clear_logs_no_logs_found():
    pass

######################################################
#
#    Getting logs
#
######################################################

def test_get_all_logs():
    pass

def test_get_log_by_date():
    pass

def test_get_log_by_date_invalid_date():
    pass

def test_get_logs_by_date_no_logs_found():
    pass

def test_get_logs_by_muscle_group():
    pass

def test_get_logs_by_muscle_group_no_logs_found():
    pass

######################################################
#
#    Updating logs
#
######################################################

def test_update_log():
    pass

def test_update_log_invalid_date():
    pass

def test_update_log_invalid_no_log_found():
    pass