import requests
import logging
from typing import List

from dataclasses import dataclass
from datetime import date

from workout.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

@dataclass
class Exercise:
    name: str
    muscle_group: int
    equipment: str
    date: date

class RecommendationsModel:
    """
    A class to manage recommending exercises to the user

    Attributes:
        target_groups (List[str]): muscle groups the user wants to focus on
        exercises (List[Exercise]): a corresponding exercise for each muscle group
        base_url (str): base url for api calls
        api_key (str): api key for api calls
    """

    def __init__(self, username):
        self.base_url: str = "https://wger.de/api/v2/exercisebaseinfo/"
        self.api_key: str = "5bf4f0a02bedae58dbbbbf318be604eb4d0f88c5"
        self.user_id: int = username
        self.target_groups: List[str] = []
        self.equipment: List[str] = []
        
######################################################
#
#    Target Group Management
#
######################################################

    def set_target_groups(self, new_groups: List[str]) -> bool:
        """
        Sets the target muscle groups for exercise recommendations.

        Args:
            new_groups (List[str]): List of muscle groups to target.

        Returns:
            bool: True if the target groups are set successfully.

        Raises:
            ValueError: If the list is empty or contains invalid entries.
        """
        if len(new_groups) == 0 or "" in new_groups:
            raise ValueError("Invalid muscle groups list provided. Muscle groups list must be non-empty.")
             
        self.target_groups = new_groups
        return True

    def add_target_group(self, new_group: str) -> bool:
        """
        Adds a new muscle group to the target groups.

        Args:
            new_group (str): Muscle group to add.

        Returns:
            bool: True if the muscle group was added, False if it already exists.

        Raises:
            ValueError: If the provided muscle group is invalid.
        """
        if len(new_group) == 0:
            raise ValueError("Invalid muscle group name provided. Muscle group name must be non-empty.")
        
        if new_group not in self.target_groups:
            self.target_groups.append(new_group)
            return True
        else:
            return False
    
    def remove_target_group(self, group: str) -> bool:
        """
        Removes a muscle group from the target groups.

        Args:
            group (str): Muscle group to remove.

        Returns:
            bool: True if the muscle group was removed, False if it was not found.

        Raises:
            ValueError: If the provided muscle group is invalid.
        """
        if len(group) == 0:
            raise ValueError("Invalid muscle group name provided. Muscle group name must be non-empty.")
        
        if group in self.target_groups:
            self.target_groups.remove(group)
            return True
        else:
            return False
        
    def get_target_groups(self) -> List[str]:
        """
        Retrieves the current list of target muscle groups.

        Returns:
            List[str]: The list of target muscle groups.
        """
        return self.target_groups

######################################################
#
#    Equipment management
#
######################################################

    def set_equipment(self, new_equipment: List[str]) -> bool:
        """
        Sets the equipment list for exercise recommendations.

        Args:
            new_equipment (List[str]): List of equipment to set.

        Returns:
            bool: True if the equipment list is set successfully.

        Raises:
            ValueError: If the list is empty or contains invalid entries.
        """
        if len(new_equipment) == 0 or "" in new_equipment:
            raise ValueError("Invalid equipment list provided. Equipment list must be non-empty.")
        
        self.equipment = new_equipment
        return True

    def add_equipment(self, new_equipment: str) -> bool:
        """
        Adds a new equipment type to the equipment list.

        Args:
            new_equipment (str): Equipment type to add.

        Returns:
            bool: True if the equipment was added, False if it already exists.

        Raises:
            ValueError: If the provided equipment is invalid.
        """
        if len(new_equipment) == 0:
            raise ValueError("Invalid equipment name provided. Equipment name must be non-empty.")
        
        if new_equipment not in self.equipment:
            self.equipment.append(new_equipment)
            return True
        else:
            return False
    
    def remove_equipment(self, equipment: str) -> bool:
        """
        Removes an equipment type from the equipment list.

        Args:
            equipment (str): Equipment type to remove.

        Returns:
            bool: True if the equipment was removed, False if it was not found.

        Raises:
            ValueError: If the provided equipment is invalid.
        """
        if len(equipment) == 0:
            raise ValueError("Invalid equipment name provided. Equipment name must be non-empty.")
        
        if equipment in self.equipment:
            self.equipment.remove(equipment)
            return True
        else:
            return False
        
    def get_equipment(self) -> List[str]:
        """
        Retrieves the current list of equipment for exercise recommendations.

        Returns:
            List[str]: The list of equipment.
        """
        return self.equipment

######################################################
#
#    External API Calls (wger api)
#
######################################################

    def get_exercises_by_many_muscle_groups(self, muscle_groups: List[str]) -> List[Exercise]:
        """
        Fetches exercises based on the user's target muscle groups.

        Args:
            muscle_groups (List[str]): List of target muscle groups.

        Returns:
            List[Exercise]: List of recommended exercises targeting the provided muscle groups.

        Raises:
            requests.RequestException: If there is an error with the API request.
        """
        params = {
            "language": 2,  # default Language: English
            "api_key": self.api_key
        }

        try:
            #response = requests.get(f"{BASE_URL}exercise/", params=params)
            response = requests.get(self.base_url, params=params, headers={"Authorization": f"Token {self.api_key}"})
            response.raise_for_status()
            data = response.json().get("results", []) # getting data

            # Recommendation logic based on time and target muscle
            recommendations: List[Exercise] = []
            
            for target in set(muscle_groups):
                for item in data:  
                    if "exercises" in item:  
                        for exercise in item["exercises"]:  
                            if exercise.get("language") == 2: 
                                if(target == 'leg') and (("squat" in exercise.get("name", "No name available").lower()) or ("running" in exercise.get("name", "No name available").lower())):
                                    name = exercise.get("name", "No name available")
                                    muscles = ", ".join([muscle["name"] for muscle in item.get("muscles", [])]) or "No muscles targeted"
                                    equipment = ", ".join([eq["name"] for eq in item.get("equipment", [])]) or "No equipment required"
                                    today_date = date.today().strftime("%Y-%m-%d")
                                    recommendations.append(Exercise(name=name, muscle_group=muscles, equipment=equipment, date = today_date)) # storing data
                                if(target == 'arm') and (("curl" in exercise.get("name", "No name available").lower()) or ("tricep" in exercise.get("name", "No name available").lower())):
                                    name = exercise.get("name", "No name available")
                                    muscles = ", ".join([muscle["name"] for muscle in item.get("muscles", [])]) or "No muscles targeted"
                                    equipment = ", ".join([eq["name"] for eq in item.get("equipment", [])]) or "No equipment required"
                                    today_date = date.today().strftime("%Y-%m-%d")
                                    recommendations.append(Exercise(name=name, muscle_group=muscles, equipment=equipment, date = today_date))
                                if(target == 'back') and (("pull" in exercise.get("name", "No name available").lower()) or ("row" in exercise.get("name", "No name available").lower())):
                                    name = exercise.get("name", "No name available")
                                    muscles = ", ".join([muscle["name"] for muscle in item.get("muscles", [])]) or "No muscles targeted"
                                    equipment = ", ".join([eq["name"] for eq in item.get("equipment", [])]) or "No equipment required"
                                    today_date = date.today().strftime("%Y-%m-%d")
                                    recommendations.append(Exercise(name=name, muscle_group=muscles, equipment=equipment, date = today_date))
                                if(target == 'abs') and (("crunch" in exercise.get("name", "No name available").lower()) or ("plank" in exercise.get("name", "No name available").lower())):
                                    name = exercise.get("name", "No name available")
                                    muscles = ", ".join([muscle["name"] for muscle in item.get("muscles", [])]) or "No muscles targeted"
                                    equipment = ", ".join([eq["name"] for eq in item.get("equipment", [])]) or "No equipment required"
                                    today_date = date.today().strftime("%Y-%m-%d")
                                    recommendations.append(Exercise(name=name, muscle_group=muscles, equipment=equipment, date = today_date))
                                if(target == 'cardio') and (("swim" in exercise.get("name", "No name available").lower()) or ("run" in exercise.get("name", "No name available").lower())):
                                    name = exercise.get("name", "No name available")
                                    muscles = ", ".join([muscle["name"] for muscle in item.get("muscles", [])]) or "No muscles targeted"
                                    equipment = ", ".join([eq["name"] for eq in item.get("equipment", [])]) or "No equipment required"
                                    today_date = date.today().strftime("%Y-%m-%d")
                                    recommendations.append(Exercise(name=name, muscle_group=muscles, equipment=equipment, date = today_date))

                                #print(f"Exercise Name: {name}")
                                #print(f"Muscle Group Targeted: {muscles}")
                                #print(f"Equipment: {equipment}")
                                #print("-" * 40)

            return recommendations
        except requests.RequestException as e:
            return [f"Error fetching exercises: {str(e)}"]
        
    def get_exercises_by_many_equipment(self, equipment_list: List[str]) -> List[Exercise]: 
        """
        Fetches exercises based on the user's preferred equipment.

        Args:
            equipment_list (List[str]): List of equipment preferences.

        Returns:
            List[Exercise]: List of recommended exercises using the provided equipment.

        Raises:
            requests.RequestException: If there is an error with the API request.
        """
        params = {
            "language": 2,  # default Language: English
            "api_key": self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params, headers={"Authorization": f"Token {self.api_key}"})
            response.raise_for_status()
            data = response.json().get("results", []) # getting data

            # Recommendation logic based on time and target muscle
            recommendations: List[Exercise] = []
            
            for target in set(equipment_list):
                for item in data:  
                    if "exercises" in item:  
                        for exercise in item["exercises"]:  
                            if exercise.get("language") == 2: 
                                name = exercise.get("name", "No name available")
                                muscles = ", ".join([muscle["name"] for muscle in item.get("muscles", [])]) or "No muscles targeted"
                                equipment = ", ".join([eq["name"] for eq in item.get("equipment", [])]) or "No equipment required"
                                today_date = date.today().strftime("%Y-%m-%d")
                                if(equipment.lower()==target):
                                    recommendations.append(Exercise(name=name, muscle_group=muscles, equipment=equipment, date = today_date))
                                if(target=='none') and (equipment=="No equipment required"):
                                    recommendations.append(Exercise(name=name, muscle_group=muscles, equipment=equipment, date = today_date))
            return recommendations
        except requests.RequestException as e:
            return [f"Error fetching exercises: {str(e)}"]
            
    # def update_one_exercise(recommendations,index,muscle):
    #     """
    #     Delete an exercise, add a new exercise, and updating the recommendations

    #     Arg:
    #         recommendations: list of the recommended exercises
    #         index: index of the exercise that the user wants to update
    #         muscle: string of which muscle group the user wants to target

    #     Return:
    #         recommendations: the new updated list of recommended exercises
    #     """
    #     params = {
    #         "language": 2,  # default Language: English
    #         "api_key": API_KEY  
    #     }

    #     try:
    #         # Fetch exercises targeting the specified muscle group
    #         fetched_exercises = fetch_exercise_by_muscle_group([muscle_group.lower()])

    #         if not fetched_exercises:
    #             print(f"No exercises found targeting '{muscle_group}'.")
    #             return recommendations

    #         if 0 <= index < len(recommendations):
    #             old_exercise = recommendations[index]
    #             new_exercise = fetched_exercises[0]  
    #             recommendations[index] = new_exercise
    #             print(f"Replaced '{old_exercise.name}' with '{new_exercise.name}'.")
    #             return recommendations
    #         else:
    #             print("Invalid index provided.")
    #             return recommendations

    #     except Exception as e:
    #         print(f"An error occurred while updating the exercise: {str(e)}")
    #         return recommendations

    #     except requests.RequestException as e:
    #         return [f"Error fetching exercises: {str(e)}"]
    
