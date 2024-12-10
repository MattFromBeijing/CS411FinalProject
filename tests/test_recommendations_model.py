from contextlib import contextmanager
import pytest
from datetime import datetime

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

######################################################
#
#    Target group managment
#
######################################################

def test_set_target_groups(recommendations_model, sample_target_group_list):
    result = recommendations_model.set_target_groups(sample_target_group_list)
    assert recommendations_model.target_groups == sample_target_group_list
    assert result == True
    
def test_set_target_groups_invalid_groups(recommendations_model):
    with pytest.raises(ValueError, match="Invalid muscle groups list provided. Muscle groups list must be non-empty."):
        recommendations_model.set_target_groups([])
        
    with pytest.raises(ValueError, match="Invalid muscle groups list provided. Muscle groups list must be non-empty."):
        recommendations_model.set_target_groups([""])
    
def test_add_target_group(recommendations_model, sample_target_group1):
    result = recommendations_model.add_target_group(sample_target_group1)
    assert recommendations_model.target_groups == [sample_target_group1]
    assert result == True
    
def test_add_target_group_duplicate(recommendations_model, sample_target_group1):
    recommendations_model.add_target_group(sample_target_group1)
    result = recommendations_model.add_target_group(sample_target_group1)
    assert recommendations_model.target_groups == [sample_target_group1]
    assert result == False
    
def test_add_target_group_invalid_group(recommendations_model):
    with pytest.raises(ValueError, match="Invalid muscle group name provided. Muscle group name must be non-empty."):
        recommendations_model.add_target_group("")
        
def test_remove_target_group(recommendations_model, sample_target_group1, sample_target_group2):
    recommendations_model.add_target_group(sample_target_group1)
    recommendations_model.add_target_group(sample_target_group2)
    assert recommendations_model.target_groups == [sample_target_group1, sample_target_group2]
    
    result = recommendations_model.remove_target_group(sample_target_group1)
    assert recommendations_model.target_groups == [sample_target_group2]
    assert result == True
    
def test_remove_target_group_not_found(recommendations_model, sample_target_group1, sample_target_group2):
    recommendations_model.add_target_group(sample_target_group1)
    assert recommendations_model.target_groups == [sample_target_group1]
    
    result = recommendations_model.remove_target_group(sample_target_group2)
    assert recommendations_model.target_groups == [sample_target_group1]
    assert result == False
    
def test_remove_target_group_invalid_groups(recommendations_model):    
    with pytest.raises(ValueError, match="Invalid muscle group name provided. Muscle group name must be non-empty."):
        recommendations_model.remove_target_group("")
        
def test_get_target_groups(recommendations_model, sample_target_group1):
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
    result = recommendations_model.set_equipment(sample_equipment_list)
    assert recommendations_model.equipment == sample_equipment_list
    assert result == True

def test_set_equipment_list_invalid(recommendations_model):
    with pytest.raises(ValueError, match="Invalid equipment list provided. Equipment list must be non-empty."):
        recommendations_model.set_equipment([])
    
    with pytest.raises(ValueError, match="Invalid equipment list provided. Equipment list must be non-empty."):
        recommendations_model.set_equipment([""])

def test_add_equipment(recommendations_model, sample_equipment1):
    result = recommendations_model.add_equipment(sample_equipment1)
    assert recommendations_model.equipment == [sample_equipment1]
    assert result == True

def test_add_equipment_duplicate(recommendations_model, sample_equipment1):
    recommendations_model.add_equipment(sample_equipment1)
    result = recommendations_model.add_equipment(sample_equipment1)
    assert recommendations_model.equipment == [sample_equipment1]
    assert result == False

def test_add_equipment_invalid(recommendations_model):
    with pytest.raises(ValueError, match="Invalid equipment name provided. Equipment name must be non-empty."):
        recommendations_model.add_equipment("")

def test_remove_equipment(recommendations_model, sample_equipment1, sample_equipment2):
    recommendations_model.add_equipment(sample_equipment1)
    recommendations_model.add_equipment(sample_equipment2)
    assert recommendations_model.equipment == [sample_equipment1, sample_equipment2]
    
    result = recommendations_model.remove_equipment(sample_equipment1)
    assert recommendations_model.equipment == [sample_equipment2]
    assert result == True

def test_remove_equipment_not_found(recommendations_model, sample_equipment1, sample_equipment2):
    recommendations_model.add_equipment(sample_equipment1)
    assert recommendations_model.equipment == [sample_equipment1]
    
    result = recommendations_model.remove_equipment(sample_equipment2)
    assert recommendations_model.equipment == [sample_equipment1]
    assert result == False

def test_remove_equipment_invalid(recommendations_model):
    with pytest.raises(ValueError, match="Invalid equipment name provided. Equipment name must be non-empty."):
        recommendations_model.remove_equipment("")
        
def test_get_equipment(recommendations_model, sample_equipment1):
    result = recommendations_model.get_equipment()
    assert result == []
    
    recommendations_model.add_equipment(sample_equipment1)
    result = recommendations_model.get_equipment()
    assert result == [sample_equipment1]
        
######################################################
#
#    API calls
#
######################################################

def test_get_exercises_by_many_muscle_groups(mocker, recommendations_model, sample_target_group_list):
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