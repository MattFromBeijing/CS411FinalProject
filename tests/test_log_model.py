from contextlib import contextmanager
import re
import pytest

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
#    Fixtures
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

    mocker.patch("workout.models.log_model.get_db_connection", mock_get_db_connection)

    return mock_cursor  # Return the mock cursor so we can set expectations per test

######################################################
#    Creating logs
######################################################

def test_create_log(mock_cursor):
    """Test creating a new log entry."""

    result = create_log(user_id=123, exercise_name="Bench Press", muscle_groups="1, 2", date="2024-12-01")

    expected_query = normalize_whitespace("""
        INSERT INTO logs (user_id, exercise_name, muscle_groups, date) 
        VALUES (?, ?, ?, ?)
    """)
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert expected_query == actual_query, f"Expected \'{expected_query}\', got {actual_query}"

    expected_arguments = (123, "Bench Press", "1, 2", "2024-12-01")
    actual_arguments = mock_cursor.execute.call_args[0][1]
    assert expected_arguments == actual_arguments, f"Expected \'{expected_arguments}\' got {actual_arguments}."

    assert result is True, "The function did not return True when log was successfully created."

def test_create_log_invalid_exercise_name(mock_cursor):
    """Test creating a new log entry with an invalid exercise_name."""

    with pytest.raises(ValueError, match="Invalid exercise name provided. exercise_name must be an string with length greater than 0."):
        create_log(user_id=123, exercise_name="", muscle_groups="1, 2", date="2024-12-01")

def test_create_log_invalid_date(mock_cursor):
    """Test creating a new log entry with an invalid date"""

    with pytest.raises(ValueError, match="Invalid date format provided: 9/12. date must be in format: YYYY-MM-DD"):
        create_log(user_id=123, exercise_name="Bench Press", muscle_groups="1, 2", date="9/12")

######################################################
#    Deleting logs
######################################################

def test_clear_logs(mock_cursor):
    """Test clearing logs for a user with logs."""
    
    mock_cursor.rowcount = 1

    result = clear_logs(123)

    expected_query = normalize_whitespace("DELETE FROM logs WHERE user_id = ?")
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert expected_query == actual_query, f"Expected \'{expected_query}\', got {actual_query}"

    expected_arguments = (123)
    actual_arguments = mock_cursor.execute.call_args[0][1]
    assert expected_arguments == actual_arguments, f"Expected \'{expected_arguments}\', got {actual_arguments}."

    assert result is True, "The function did not return True when logs were successfully cleared."

def test_clear_logs_no_logs_found(mock_cursor):
    """Test clearing logs for a user with no logs."""

    mock_cursor.rowcount = 0

    with pytest.raises(ValueError, match="No logs found for user_id=123"):
        clear_logs(123)

######################################################
#    Getting logs
######################################################

def test_get_all_logs(mock_cursor):
    """Test getting all logs from a user with logs."""

    mock_cursor.fetchall.return_value = [
        (1, 123, "Bench Press", "1, 2", "2024-12-01"),
        (2, 123, "Squat", "3, 4", "2024-12-02")
    ]
    
    result = get_all_logs(123)

    expected_query = normalize_whitespace("SELECT * FROM logs WHERE user_id = ?")
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert expected_query == actual_query, f"Expected \'{expected_query}\', got {actual_query}"

    expected_arguments = (123,)
    actual_arguments = mock_cursor.execute.call_args[0][1]
    assert expected_arguments == actual_arguments, f"Expected \'{expected_arguments}\', got {actual_arguments}."

    expected_result = [
        Log(id=1, user_id=123, exercise_name="Bench Press", muscle_groups="1, 2", date="2024-12-01"),
        Log(id=2, user_id=123, exercise_name="Squat", muscle_groups="3, 4", date="2024-12-02")
    ]
    assert expected_result == result, f"Expected \'{expected_result}\', got \'{result}\' when logs were successfully retrieved."

def test_get_all_logs_no_logs(mock_cursor):
    """Test getting all logs from a user with no logs."""

    result = get_all_logs(123)

    expected_query = normalize_whitespace("SELECT * FROM logs WHERE user_id = ?")
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert expected_query == actual_query, f"Expected \'{expected_query}\', got {actual_query}"

    expected_arguments = (123,)
    actual_arguments = mock_cursor.execute.call_args[0][1]
    assert expected_arguments == actual_arguments, f"Expected \'{expected_arguments}\', got {actual_arguments}."

    expected_result = []
    assert expected_result == result, f"Expected \'{expected_result}\', got \'{result}\' when logs were successfully retrieved."

def test_get_log_by_date(mock_cursor):
    """Test getting a log from a user with logs by date."""

    mock_cursor.fetchone.return_value = (1, 123, "Bench Press", "1, 2", "2024-12-01")

    result = get_log_by_date(123, "2024-12-01")

    expected_query = normalize_whitespace("SELECT * FROM logs WHERE user_id = ? AND date = ?")
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert expected_query == actual_query, f"Expected \'{expected_query}\', got {actual_query}"

    expected_arguments = (123, "2024-12-01")
    actual_arguments = mock_cursor.execute.call_args[0][1]
    assert expected_arguments == actual_arguments, f"Expected \'{expected_arguments}\', got {actual_arguments}."

    expected_result = Log(1, 123, "Bench Press", "1, 2", "2024-12-01")
    assert expected_result == result, f"Expected \'{expected_result}\', got \'{result}\' when logs were successfully retrieved."

def test_get_log_by_date_invalid_date(mock_cursor):
    """Test getting all logs from a user with invalid date."""

    with pytest.raises(ValueError, match="Invalid date format provided: \'9/12\'. date must be in format: YYYY-MM-DD"):
        get_log_by_date(123, "9/12")

def test_get_logs_by_date_no_log_found(mock_cursor):
    """Test getting a log from a user with no logs by date."""

    mock_cursor.fetchone.return_value = None

    result = get_log_by_date(123, "2024-12-01")

    expected_query = normalize_whitespace("SELECT * FROM logs WHERE user_id = ? AND date = ?")
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert expected_query == actual_query, f"Expected \'{expected_query}\', got {actual_query}"

    expected_arguments = (123, "2024-12-01")
    actual_arguments = mock_cursor.execute.call_args[0][1]
    assert expected_arguments == actual_arguments, f"Expected \'{expected_arguments}\', got {actual_arguments}."

    expected_result = None
    assert expected_result == result, f"Expected \'{expected_result}\', got \'{result}\' when logs were successfully retrieved."

def test_get_logs_by_muscle_groups(mock_cursor):
    """Test getting all logs from a user with logs by muscle_groups."""

    mock_cursor.fetchall.return_value = [
        (1, 123, "Leg Press", "3, 4", "2024-12-01"),
        (2, 123, "Squat", "3", "2024-12-02")
    ]

    result = get_logs_by_muscle_group(123, "3, 4")

    expected_query = normalize_whitespace("SELECT * FROM logs WHERE user_id = ? AND (muscle_groups LIKE ? OR muscle_groups LIKE ?)")
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert expected_query == actual_query, f"Expected \'{expected_query}\', got {actual_query}"

    expected_arguments = [123, "%3%" , "%4%"]
    actual_arguments = mock_cursor.execute.call_args[0][1]
    assert expected_arguments == actual_arguments, f"Expected \'{expected_arguments}\', got {actual_arguments}."

    expected_result = [
        Log(1, 123, "Leg Press", "3, 4", "2024-12-01"),
        Log(2, 123, "Squat", "3", "2024-12-02")
    ]
    assert expected_result == result, f"Expected \'{expected_result}\', got \'{result}\' when logs were successfully retrieved."    

def test_get_logs_by_muscle_group_empty_muscle_groups():
    """Test getting all logs from a user with no logs by muscle_groups."""

    result = get_logs_by_muscle_group(123, "")
    expected_result = []
    assert expected_result == result, f"Expected \'{expected_result}\', got \'{result}\' when logs were successfully retrieved." 

def test_get_logs_by_muscle_group_no_logs_found(mock_cursor):
    """Test getting all logs from a user with no logs by muscle_groups."""

    mock_cursor.fetchall.return_value = []

    result = get_logs_by_muscle_group(123, "3, 4")

    expected_query = normalize_whitespace("SELECT * FROM logs WHERE user_id = ? AND (muscle_groups LIKE ? OR muscle_groups LIKE ?)")
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert expected_query == actual_query, f"Expected \'{expected_query}\', got {actual_query}"

    expected_arguments = [123, "%3%" , "%4%"]
    actual_arguments = mock_cursor.execute.call_args[0][1]
    assert expected_arguments == actual_arguments, f"Expected \'{expected_arguments}\', got {actual_arguments}."

    expected_result = []
    assert expected_result == result, f"Expected \'{expected_result}\', got \'{result}\' when logs were successfully retrieved." 

######################################################
#    Updating logs
######################################################

def test_update_log(mock_cursor):
    """Test updating a log from a user with logs."""

    mock_cursor.rowcount = 1

    result = update_log(123, "2024-12-01", "Leg press", "3, 4")

    expected_query = normalize_whitespace("UPDATE logs SET exercise_name = ?, muscle_groups = ? WHERE user_id = ? AND date = ?")
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert expected_query == actual_query, f"Expected \'{expected_query}\', got {actual_query}"

    expected_arguments = ("Leg press", "3, 4", 123, "2024-12-01")
    actual_arguments = mock_cursor.execute.call_args[0][1]
    assert expected_arguments == actual_arguments, f"Expected \'{expected_arguments}\', got {actual_arguments}."

    assert result is True, "The function did not return True when logs were successfully cleared."

def test_update_log_invalid_date(mock_cursor):
    """Test updating a log with an invalid date."""

    mock_cursor.rowcount = 0

    with pytest.raises(ValueError, match="Invalid date format provided: \'9/12\'. date must be in format: YYYY-MM-DD"):
        update_log(user_id=123, exercise_name="Bench press", muscle_groups="1, 2", date="9/12")

def test_update_log_no_log_found(mock_cursor):
    """Test updating a log for a user with no logs."""

    mock_cursor.rowcount = 0

    with pytest.raises(ValueError, match="No log found for user_id=123 and date=2024-12-01"):
        update_log(user_id=123, exercise_name="Bench press", muscle_groups="1, 2", date="2024-12-01")