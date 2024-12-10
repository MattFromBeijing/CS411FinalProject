import requests
import os
import sys
from dataclasses import dataclass
from datetime import date
#from workout.models.exercise_model import Exercise
@dataclass
class Exercise:
    name: str
    muscle_group: int
    equipment: str
    date: date

# Base URL for the wger API
BASE_URL = "https://wger.de/api/v2/exercisebaseinfo/"

API_KEY = "5bf4f0a02bedae58dbbbbf318be604eb4d0f88c5"

'''def fetch_exercises_by_weights(current_weight, desired_weight):
    """
    Fetch recommended exercises based on the user's current and desired weights.

    ARG: 
        current_weight = integer of users current weight 
        desired_weight = integer of users desired weight

    
    Return: List of recommended exercises
    """
    params = {"language": 2}  # default Language: English

    try:
        response = requests.get(f"{BASE_URL}exercise/", params=params)
        response.raise_for_status()
        data = response.json().get("results", []) # getting data

        # Recommendation logic based on weight difference, lose or gain weight or maintain
        recommendations = []
        weight_difference = current_weight - desired_weight

        # current logic for exercise recommendations, might change this
        for exercise in data:
            if weight_difference > 0:  # User wants to lose weight/fat
                # exercises involving cardio and calorie burning
                if "cardio" in exercise["description"].lower() or "endurance" in exercise["description"].lower():
                    recommendations.append(exercise["name"])
            elif weight_difference < 0:  # User wants to gain weight/muscle
                # exercises to build muscle 
                if "strength" in exercise["description"].lower() or "muscle" in exercise["description"].lower():
                    recommendations.append(exercise["name"])
            else:  # Maintenance
                # maintaining current weight and size
                if "flexibility" in exercise["description"].lower() or "general" in exercise["description"].lower():
                    recommendations.append(exercise["name"])

        return recommendations if recommendations else ["No suitable exercises found."]
    except requests.RequestException as e:
        return [f"Error fetching exercises: {str(e)}"]'''

def fetch_exercise_by_muscle_group(list_of_muscle_group):
    """
    Fetch exercises based on the user's target muscle groups. Recommend exercises based on time constraint and target muscle

    Arg:
        list_of_muscle_group: list of target muscle from user

    Return:
        recommendations: list of recommended exercises
    """
    params = {
        "language": 2,  # default Language: English
        "api_key": API_KEY  
    }

    try:
        #response = requests.get(f"{BASE_URL}exercise/", params=params)
        response = requests.get(BASE_URL, params=params, headers={"Authorization": f"Token {API_KEY}"})
        response.raise_for_status()
        data = response.json().get("results", []) # getting data
        
        print(data)

        # Recommendation logic based on time and target muscle
        recommendations = []
        
        for target in list_of_muscle_group:
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

                            # printing statements
                            #print(f"Exercise Name: {name}")
                            #print(f"Muscle Group Targeted: {muscles}")
                            #print(f"Equipment: {equipment}")
                            #print("-" * 40)

        return recommendations
    except requests.RequestException as e:
        return [f"Error fetching exercises: {str(e)}"]

def fetch_exercises_by_equipments(equipmentslist): 
    '''
    Fetch exercises based on the user's preferred equipements

    Arg:
        equipments: list of equipments

    Return:
        recommendations: list of recommended exercises
    '''
    params = {
        "language": 2,  # default Language: English
        "api_key": API_KEY  
    }

    try:
        #response = requests.get(f"{BASE_URL}exercise/", params=params)
        response = requests.get(BASE_URL, params=params, headers={"Authorization": f"Token {API_KEY}"})
        response.raise_for_status()
        data = response.json().get("results", []) # getting data
        
        print(data)

        # Recommendation logic based on time and target muscle
        recommendations = []
        
        for target in equipmentslist:
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


def update_one_exercise(recommendations,index,muscle):
    """
    Delete an exercise, add a new exercise, and updating the recommendations

    Arg:
        recommendations: list of the recommended exercises
        index: index of the exercise that the user wants to update
        muscle: string of which muscle group the user wants to target

    Return:
        recommendations: the new updated list of recommended exercises
    """
    params = {
        "language": 2,  # default Language: English
        "api_key": API_KEY  
    }

    try:
        # Fetch exercises targeting the specified muscle group
        fetched_exercises = fetch_exercise_by_muscle_group([muscle_group.lower()])

        if not fetched_exercises:
            print(f"No exercises found targeting '{muscle_group}'.")
            return recommendations

        if 0 <= index < len(recommendations):
            old_exercise = recommendations[index]
            new_exercise = fetched_exercises[0]  
            recommendations[index] = new_exercise
            print(f"Replaced '{old_exercise.name}' with '{new_exercise.name}'.")
            return recommendations
        else:
            print("Invalid index provided.")
            return recommendations

    except Exception as e:
        print(f"An error occurred while updating the exercise: {str(e)}")
        return recommendations

    except requests.RequestException as e:
        return [f"Error fetching exercises: {str(e)}"]



if __name__ == "__main__":
    try:
        choice = input("Recommend exercises based on muscle or equipments: ").lower()
        while(choice!="muscle") and (choice!="equipments"):
            print("please choose between muscle or equipments")
            choice = input("Recommend exercises based on muscle or equipment: ")
        if(choice == "muscle"):
            print("\nPlease specify the muscle groups you'd like to target during your workout.")
            print("\nPlease choose only from the following: leg, arm, back, abs, cardio")
            while True:
                valid_muscles = {"leg", "arm", "back", "abs", "cardio"}
                target_muscle_groups = input("Enter your preferred muscle groups, separated by commas: ").strip().lower()
                muscle_groups_list = {muscle.strip() for muscle in target_muscle_groups.split(",")}

                if muscle_groups_list.issubset(valid_muscles) and muscle_groups_list:
                    break  
                else:
                    print("\nInvalid selection. Please choose only from the following: leg, arm, back, abs, cardio")

            print("\nFetching exercise recommendations...")
            exercises = fetch_exercise_by_muscle_group(muscle_groups_list)
            print(f"\nRecommended Exercises Targeting: {', '.join(muscle_groups_list)}")
        
        if(choice == "equipments"):
            print("\nPlease specify the equipment(s) you'd like to use during your workout.")
            print("\nPlease choose only from the following: dumbbell, mat, bench, kettlebell, none")
            while True:
                valid_equipment = {"dumbbell", "mat", "bench", "kettlebell", "none"}
                equipments = input("Enter your preferred equipments, separated by commas: ").strip().lower()
                equipments_list = {equipment.strip() for equipment in equipments.split(",")}

                if equipments_list.issubset(valid_equipment) and equipments_list:
                    break  
                else:
                    print("\nInvalid selection. Please choose only from the following: dumbbell, mat, bench, kettlebell, none")

            print("\nFetching exercise recommendations...")
            exercises = fetch_exercises_by_equipments(equipments_list)
            print(f"\nRecommended Exercises Using: {', '.join(equipments_list)}")

        for exercise in exercises:
            print(f"- {exercise}")

        # Ask user if they want to update an exercise
        if exercises:
            update_choice = input("\nWould you like to update a specific exercise? (yes/no): ").strip().lower()
            if update_choice == "yes":
                print("\nYour Current Exercise Recommendations:")
                for idx, ex in enumerate(exercises, start=1):
                    print(f"{idx}. {ex}")

                try:
                    # Get user input for updating an exercise
                    exercise_to_update = input("\nEnter the index of the exercise you want to replace: ").strip() # returns an integer
                    muscle_group = input("Enter the muscle group you'd like the new exercise to target: ").strip().lower()

                    index = int(exercise_to_update) - 1
                    if index < len(exercises):
                        updated_recommendations = update_one_exercise(exercises, index, muscle_group)
                        print("\nUpdated Exercise Recommendations:")
                        for exercise in updated_recommendations:
                            print(f"- {exercise}")
                    else:
                        print("\nThe exercise you entered is not in the current recommendations.")

                except ValueError:
                    print("\nInvalid input. Please try again.")

    except ValueError:
        print("\nInvalid input. Please enter valid numbers for your workout time.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")

