import pytest
import unittest
from unittest.mock import patch
from datetime import date
from workout.models.user_model import get_db_connection, Exercise
from workout.models.exercise_model import get_exercises_by_one_muscle_group 

@pytest.fixture
def mock_get_exercises():
    """Mock the API response for exercises."""
    mock_data = {
        "results": [
            {
                "exercises": [
                    {
                        "name": "Squat",
                        "muscles": [{"name": "leg"}],
                        "equipment": [{"name": "none"}],
                        "language": 2
                    },
                    {
                        "name": "Running",
                        "muscles": [{"name": "leg"}],
                        "equipment": [{"name": "none"}],
                        "language": 2
                    },
                    {
                        "name": "Bicep Curl",
                        "muscles": [{"name": "arm"}],
                        "equipment": [{"name": "dumbbell"}],
                        "language": 2
                    }
                ]
            }
        ]
    }
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_data
        yield mock_get

def test_get_exercises_by_one_muscle_group_success(mock_get_exercises):
    """Test that the correct exercises are returned for the specified muscle group."""
    muscle_group = 'leg'
    exercises = get_exercises_by_one_muscle_group(muscle_group)
    
    assert len(exercises) == 2
    assert exercises[0].name == "Squat"
    assert exercises[1].name == "Running"
    assert exercises[0].muscle_group == "leg"
    assert exercises[1].muscle_group == "leg"
    assert exercises[0].equipment == "none"
    assert exercises[1].equipment == "none"

def test_get_exercises_by_one_muscle_group_no_match(mock_get_exercises):
    """Test when no exercises match the specified muscle group."""
    muscle_group = 'back'
    exercises = get_exercises_by_one_muscle_group(muscle_group)
    
    assert len(exercises) == 0

def test_get_exercises_by_one_muscle_group_api_error():
    """Test when the API request fails."""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.RequestException("API request failed")
        
        exercises = get_exercises_by_one_muscle_group('leg')
        assert exercises == ["Error fetching exercises: API request failed"]

def test_get_exercises_by_one_muscle_group_empty_response():
    """Test when the API returns an empty list."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"results": []}
        
        exercises = get_exercises_by_one_muscle_group('leg')
        assert len(exercises) == 0
