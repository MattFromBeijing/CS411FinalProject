from contextlib import contextmanager
import pytest
import requests
from datetime import datetime
from datetime import date

from workout.models.recommendations_model import (
    Exercise,
    RecommendationsModel,
)

######################################################
#
#    Fixtures
#
######################################################

@pytest.fixture()
def recommendations_model():
    return RecommendationsModel("Matthew")

@pytest.fixture
def sample_target_group1():
    return "leg"

@pytest.fixture
def sample_target_group2():
    return "arm"

@pytest.fixture
def sample_target_group_list():
    return ["leg", "arm"]

@pytest.fixture
def sample_equipment1():
    return "dumbbell"

@pytest.fixture
def sample_equipment2():
    return "kettlebell"

@pytest.fixture
def sample_equipment_list():
    return ["dumbbell", "kettlebell"]

@pytest.fixture
def sample_target_song1():
    return "Song A"

@pytest.fixture
def sample_target_song2():
    return "Song B"

@pytest.fixture
def sample_target_song_list():
    return ["Song A", "Song B"]

######################################################
#
#    Target group managment
#
######################################################

def test_set_target_groups(recommendations_model, sample_target_group_list):
    """Test setting multiple target muscle groups at once."""
    result = recommendations_model.set_target_groups(sample_target_group_list)
    assert recommendations_model.target_groups == sample_target_group_list
    assert result == True
    
def test_set_target_groups_invalid_groups(recommendations_model):
    """Test setting invalid muscle groups."""
    with pytest.raises(ValueError, match="Invalid muscle groups list provided. Muscle groups list must be non-empty."):
        recommendations_model.set_target_groups([])
        
    with pytest.raises(ValueError, match="Invalid muscle groups list provided. Muscle groups list must be non-empty."):
        recommendations_model.set_target_groups([""])
    
def test_add_target_group(recommendations_model, sample_target_group1):
    """Test adding a single target muscle group."""
    result = recommendations_model.add_target_group(sample_target_group1)
    assert recommendations_model.target_groups == [sample_target_group1]
    assert result == True
    
def test_add_target_group_duplicate(recommendations_model, sample_target_group1):
    """Test adding a duplicate target muscle group."""
    recommendations_model.add_target_group(sample_target_group1)
    result = recommendations_model.add_target_group(sample_target_group1)
    assert recommendations_model.target_groups == [sample_target_group1]
    assert result == False
    
def test_add_target_group_invalid_group(recommendations_model):
    """Test adding an invalid target muscle group."""
    with pytest.raises(ValueError, match="Invalid muscle group name provided. Muscle group name must be non-empty."):
        recommendations_model.add_target_group("")
        
def test_remove_target_group(recommendations_model, sample_target_group1, sample_target_group2):
    """Test removing a target muscle group."""
    recommendations_model.add_target_group(sample_target_group1)
    recommendations_model.add_target_group(sample_target_group2)
    assert recommendations_model.target_groups == [sample_target_group1, sample_target_group2]
    
    result = recommendations_model.remove_target_group(sample_target_group1)
    assert recommendations_model.target_groups == [sample_target_group2]
    assert result == True
    
def test_remove_target_group_not_found(recommendations_model, sample_target_group1, sample_target_group2):
    """Test removing a muscle group not in the target groups."""
    recommendations_model.add_target_group(sample_target_group1)
    assert recommendations_model.target_groups == [sample_target_group1]
    
    result = recommendations_model.remove_target_group(sample_target_group2)
    assert recommendations_model.target_groups == [sample_target_group1]
    assert result == False
    
def test_remove_target_group_invalid_groups(recommendations_model):
    """Test removing an invalid muscle group."""
    with pytest.raises(ValueError, match="Invalid muscle group name provided. Muscle group name must be non-empty."):
        recommendations_model.remove_target_group("")
        
def test_get_target_groups(recommendations_model, sample_target_group1):
    """Test retrieving the list of target muscle groups."""
    result = recommendations_model.get_target_groups()
    assert result == []
    
    recommendations_model.add_target_group(sample_target_group1)
    result = recommendations_model.get_target_groups()
    assert result == [sample_target_group1]
        
######################################################
#
#    Equipment management
#
######################################################

def test_set_equipment(recommendations_model, sample_equipment_list):
    """Test setting multiple equipment types."""
    result = recommendations_model.set_equipment(sample_equipment_list)
    assert recommendations_model.equipment == sample_equipment_list
    assert result == True

def test_set_equipment_list_invalid(recommendations_model):
    """Test setting an invalid equipment list."""
    with pytest.raises(ValueError, match="Invalid equipment list provided. Equipment list must be non-empty."):
        recommendations_model.set_equipment([])
    
    with pytest.raises(ValueError, match="Invalid equipment list provided. Equipment list must be non-empty."):
        recommendations_model.set_equipment([""])

def test_add_equipment(recommendations_model, sample_equipment1):
    """Test adding a single equipment type."""
    result = recommendations_model.add_equipment(sample_equipment1)
    assert recommendations_model.equipment == [sample_equipment1]
    assert result == True

def test_add_equipment_duplicate(recommendations_model, sample_equipment1):
    """Test adding a duplicate equipment type."""
    recommendations_model.add_equipment(sample_equipment1)
    result = recommendations_model.add_equipment(sample_equipment1)
    assert recommendations_model.equipment == [sample_equipment1]
    assert result == False

def test_add_equipment_invalid(recommendations_model):
    """Test adding an invalid equipment type."""
    with pytest.raises(ValueError, match="Invalid equipment name provided. Equipment name must be non-empty."):
        recommendations_model.add_equipment("")

def test_remove_equipment(recommendations_model, sample_equipment1, sample_equipment2):
    """Test removing an equipment type."""
    recommendations_model.add_equipment(sample_equipment1)
    recommendations_model.add_equipment(sample_equipment2)
    assert recommendations_model.equipment == [sample_equipment1, sample_equipment2]
    
    result = recommendations_model.remove_equipment(sample_equipment1)
    assert recommendations_model.equipment == [sample_equipment2]
    assert result == True

def test_remove_equipment_not_found(recommendations_model, sample_equipment1, sample_equipment2):
    """Test removing an equipment type not in the list."""
    recommendations_model.add_equipment(sample_equipment1)
    assert recommendations_model.equipment == [sample_equipment1]
    
    result = recommendations_model.remove_equipment(sample_equipment2)
    assert recommendations_model.equipment == [sample_equipment1]
    assert result == False

def test_remove_equipment_invalid(recommendations_model):
    """Test removing an invalid equipment type."""
    with pytest.raises(ValueError, match="Invalid equipment name provided. Equipment name must be non-empty."):
        recommendations_model.remove_equipment("")
        
def test_get_equipment(recommendations_model, sample_equipment1):
    """Test retrieving the list of equipment types."""
    result = recommendations_model.get_equipment()
    assert result == []
    
    recommendations_model.add_equipment(sample_equipment1)
    result = recommendations_model.get_equipment()
    assert result == [sample_equipment1]

######################################################
#
#    target songs
#
######################################################

def test_set_target_songs(song_recommendation_manager, sample_song_list):
    """Test setting multiple target songs at once."""
    result = song_recommendation_manager.set_target_songs(sample_song_list)
    assert song_recommendation_manager.target_songs == sample_song_list
    assert result is True

def test_set_target_songs_invalid_songs(song_recommendation_manager):
    """Test setting invalid songs."""
    with pytest.raises(ValueError, match="Invalid songs list provided. Songs list must be non-empty."):
        song_recommendation_manager.set_target_songs([])
        
    with pytest.raises(ValueError, match="Invalid songs list provided. Songs list must be non-empty."):
        song_recommendation_manager.set_target_songs([""])

def test_add_target_song(song_recommendation_manager, sample_song1):
    """Test adding a single target song."""
    result = song_recommendation_manager.add_target_song(sample_song1)
    assert song_recommendation_manager.target_songs == [sample_song1]
    assert result is True

def test_add_target_song_duplicate(song_recommendation_manager, sample_song1):
    """Test adding a duplicate target song."""
    song_recommendation_manager.add_target_song(sample_song1)
    result = song_recommendation_manager.add_target_song(sample_song1)
    assert song_recommendation_manager.target_songs == [sample_song1]
    assert result is False

def test_add_target_song_invalid_song(song_recommendation_manager):
    """Test adding an invalid target song."""
    with pytest.raises(ValueError, match="Invalid song name provided. Song name must be non-empty."):
        song_recommendation_manager.add_target_song("")

def test_remove_target_song(song_recommendation_manager, sample_song1, sample_song2):
    """Test removing a target song."""
    song_recommendation_manager.add_target_song(sample_song1)
    song_recommendation_manager.add_target_song(sample_song2)
    assert song_recommendation_manager.target_songs == [sample_song1, sample_song2]
    
    result = song_recommendation_manager.remove_target_song(sample_song1)
    assert song_recommendation_manager.target_songs == [sample_song2]
    assert result is True

def test_remove_target_song_not_found(song_recommendation_manager, sample_song1, sample_song2):
    """Test removing a song not in the target songs."""
    song_recommendation_manager.add_target_song(sample_song1)
    assert song_recommendation_manager.target_songs == [sample_song1]
    
    result = song_recommendation_manager.remove_target_song(sample_song2)
    assert song_recommendation_manager.target_songs == [sample_song1]
    assert result is False

def test_remove_target_song_invalid_song(song_recommendation_manager):
    """Test removing an invalid song."""
    with pytest.raises(ValueError, match="Invalid song name provided. Song name must be non-empty."):
        song_recommendation_manager.remove_target_song("")

def test_get_target_songs(song_recommendation_manager, sample_song1):
    """Test retrieving the list of target songs."""
    result = song_recommendation_manager.get_target_songs()
    assert result == []
    
    song_recommendation_manager.add_target_song(sample_song1)
    result = song_recommendation_manager.get_target_songs()
    assert result == [sample_song1]
        
######################################################
#
#    API calls
#
######################################################

def test_get_exercises_by_many_muscle_groups(mocker, recommendations_model, sample_target_group_list):
    """Test fetching exercises based on multiple muscle groups."""
    mock_response = mocker.patch("requests.get")
    mock_response.return_value.status_code = 200
    mock_response.return_value.json.return_value = {
        "results": [
            {
                "id": 229,
                "uuid": "30b2631d-d7ec-415c-800b-7eb082314c0a",
                "exercise_base": 849,
                "exercise_base_uuid": "fb0c8c53-27ec-4aac-ab6e-403b7d7f250b",
                "image": "https://wger.de/media/exercise-images/849/30b2631d-d7ec-415c-800b-7eb082314c0a.gif",
                "is_main": False,
                "style": "4",
                "license": 2,
                "license_title": "",
                "license_object_url": "",
                "license_author": "enros7500",
                "license_author_url": "",
                "license_derivative_source_url": "",
                "author_history": ["enros7500"],
                "exercises": [
                    {
                        "id": 1101,
                        "uuid": "257fdd82-bd43-4a29-81e8-c1d6ec62987d",
                        "name": "Barbell Squat",
                        "exercise_base": 849,
                        "description": "Control the descent, go down in 2 seconds and go up as explosively as you can.\nIt is very important that you do hip mobility before you start training, to improve depth.\nForget about the weight, go down as far as you can, without lifting your heels off the ground and go up.\nA good technique will generate more hypertrophy than a lot of weight without a correct ROM.",
                        "created": "2023-08-06T10:17:17.349574+02:00",
                        "language": 2,
                        "aliases": [],
                        "notes": [],
                        "license": 2,
                        "license_title": "",
                        "license_object_url": "",
                        "license_author": "enros7500",
                        "license_author_url": "",
                        "license_derivative_source_url": "",
                        "author_history": ["enros7500"]
                    }
                ]
            }
        ]
    }
    result = recommendations_model.get_exercises_by_many_muscle_groups(sample_target_group_list)
    
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    expected_results = [Exercise(name='Barbell Squat', muscle_group='No muscles targeted', equipment='No equipment required', date=formatted_date)]
    
    assert result == expected_results

def test_get_exercises_by_many_equipment(mocker, recommendations_model, sample_equipment_list):
    """Test fetching exercises based on multiple equipment types."""
    mock_response = mocker.patch("requests.get")
    mock_response.return_value.status_code = 200
    mock_response.return_value.json.return_value = {
        "results": [
            {
                "id": 31,
                "uuid": "f2733700-aa5d-4df7-bc52-1876ab4fb479",
                "created": "2023-08-06T10:17:17.422900+02:00",
                "last_update": "2024-01-17T11:21:01.706493+01:00",
                "last_update_global": "2024-01-17T11:21:01.908320+01:00",
                "category": {
                    "id": 8,
                    "name": "Arms"
                },
                "muscles": [],
                "muscles_secondary": [],
                "equipment": [
                    {
                    "id": 3,
                    "name": "Dumbbell"
                    }
                ],
                "license": {
                    "id": 1,
                    "full_name": "Creative Commons Attribution Share Alike 3",
                    "short_name": "CC-BY-SA 3",
                    "url": "https://creativecommons.org/licenses/by-sa/3.0/deed.en"
                },
                "license_author": "GrosseHund",
                "images": [],
                "exercises": [
                    {
                        "id": 289,
                        "uuid": "6add5973-86d0-4543-928a-6bb8b3f34efc",
                        "name": "Axe Hold",
                        "exercise_base": 31,
                        "description": "<p>Grab dumbbells and extend arms to side and hold as long as you can</p>",
                        "created": "2023-08-06T10:17:17.349574+02:00",
                        "language": 2,
                        "aliases": [],
                        "notes": [],
                        "license": 1,
                        "license_title": "",
                        "license_object_url": "",
                        "license_author": "GrosseHund",
                        "license_author_url": "",
                        "license_derivative_source_url": "",
                        "author_history": ["GrosseHund"]
                    },
                    {
                        "id": 677,
                        "uuid": "8e9d8968-323d-468c-9174-8cf11a105fad",
                        "name": "Axe Hold",
                        "exercise_base": 31,
                        "description": "<p>Nehmen Sie die Hanteln und strecken Sie die Arme zur Seite. Halten Sie sie so lange wie möglich.</p>",
                        "created": "2023-08-06T10:17:17.349574+02:00",
                        "language": 1,
                        "aliases": [],
                        "notes": [],
                        "license": 1,
                        "license_title": "",
                        "license_object_url": "",
                        "license_author": "GrosseHund",
                        "license_author_url": "",
                        "license_derivative_source_url": "",
                        "author_history": ["Wunschcoach", "GrosseHund"]
                    }
                ],
                "variations": None,
                "videos": [],
                "author_history": ["GrosseHund"],
                "total_authors_history": ["Wunschcoach", "GrosseHund"]
            }
        ]
    }
    result = recommendations_model.get_exercises_by_many_equipment(sample_equipment_list)
    
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    expected_results = [Exercise(name='Axe Hold', muscle_group='No muscles targeted', equipment='Dumbbell', date=formatted_date)]
    
    assert result == expected_results


def test_update_one_exercise(mocker, recommendations_model, sample_recommendations, sample_muscle_group, mock_api_response):
    """Test updating an exercise in the recommendations list."""
    mocker.patch("requests.get", return_value=mock_api_response)
    
    assert len(sample_recommendations) == 2
    
    updated_recommendations = recommendations_model.update_one_exercise(sample_recommendations, 0, sample_muscle_group)
    
    assert len(updated_recommendations) == 2 
    assert updated_recommendations[0].name == "Barbell Squat" 
    assert updated_recommendations[0].muscle_group == "Legs"
    assert updated_recommendations[0].equipment == "Barbell"
    assert updated_recommendations[0].date == date.today().strftime("%Y-%m-%d")
    
    assert updated_recommendations[1].name == "Push-up"

def test_update_one_exercise_invalid_index(mocker, recommendations_model, sample_recommendations, sample_muscle_group, mock_api_response):
    """Test updating an exercise with an invalid index."""
    mocker.patch("requests.get", return_value=mock_api_response)
    
    updated_recommendations = recommendations_model.update_one_exercise(sample_recommendations, 10, sample_muscle_group)
    
    assert len(updated_recommendations) == 2  
    assert updated_recommendations[0].name == "Squat" 
    assert updated_recommendations[1].name == "Push-up"  


######################################################
#
#    External API Calls (jamendo music api)
#
######################################################

@pytest.fixture
def mock_jamendo_response():
    """Fixture to return a mock response for the Jamendo API."""
    return {
        "results": [
            {
                "name": "Song A",
                "artist_name": "Artist A",
                "duration": 300
            },
            {
                "name": "Song B",
                "artist_name": "Artist B",
                "duration": 150
            },
            {
                "name": "Song C",
                "artist_name": "Artist C",
                "duration": 500
            }
        ]
    }

# Test for fetch_songs_based_on_workouts function
def test_fetch_songs_based_on_workouts(mocker, mock_jamendo_response,recommendations_model):
    """Test fetching songs based on workout count."""
    workout_count = 5  # Example workout count
    
    mocker.patch("requests.get", return_value=mock_jamendo_response)
    
    expected_songs = ["Song C by Artist C"]
    
    result = recommendations_model.fetch_songs_based_on_workouts(workout_count)
    
    assert result == expected_songs

def test_fetch_songs_based_on_workouts_no_results(mocker,recommendations_model):
    """Test the behavior when no songs match the criteria."""
    workout_count = 1  # Example workout count
    
    mocker.patch("requests.get", return_value={"results": []})
    
    result = recommendations_model.fetch_songs_based_on_workouts(workout_count)
    
    assert result == ["No songs found for the given criteria."]

def test_fetch_songs_based_on_workouts_api_error(mocker,recommendations_model):
    """Test handling API request errors."""
    workout_count = 3  # Example workout count
    
    mocker.patch("requests.get", side_effect=requests.exceptions.RequestException("API error"))
    
    result = recommendations_model.fetch_songs_based_on_workouts(workout_count)
    
    assert result == ["An error occurred: API error"]

# Test for fetch_random_song function
def test_fetch_random_song(mocker, mock_jamendo_response,recommendations_model):
    """Test fetching a random song."""
    
    mocker.patch("requests.get", return_value=mock_jamendo_response)
    
    result = recommendations_model.fetch_random_song()
    
    assert "by" in result  

def test_fetch_random_song_no_results(mocker,recommendations_model):
    """Test the behavior when no songs are available."""
    
    mocker.patch("requests.get", return_value={"results": []})
    
    result = recommendations_model.fetch_random_song()
    
    assert result == "No songs found."

def test_fetch_random_song_api_error(mocker,recommendations_model):
    """Test handling API request errors."""
    
    mocker.patch("requests.get", side_effect=requests.exceptions.RequestException("API error"))
    
    result = recommendations_model.fetch_random_song()
    
    assert result == "An error occurred: API error"