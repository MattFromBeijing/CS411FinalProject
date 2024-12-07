import requests
import os
from dataclasses import dataclass
from datetime import date
from workout.models.exercise_model import Exercise

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

        # Recommendation logic based on time and target muscle
        recommendations = []

        for item in data:  
            if "exercises" in item:  
                for exercise in item["exercises"]:  
                    if exercise.get("language") == 2: 
                        name = exercise.get("name", "No name available")
                        muscles = ", ".join([muscle["name"] for muscle in item.get("muscles", [])]) or "No muscles targeted"
                        equipment = ", ".join([eq["name"] for eq in item.get("equipment", [])]) or "No equipment required"

                        recommendations.append(Exercise(name=name, muscle_group=muscles, equipment=equipment)) # storing data

                        # printing statements
                        '''print(f"Exercise Name: {name}")
                        print(f"Muscle Group Targeted: {muscles}")
                        print(f"Equipment: {equipment}")
                        print("-" * 40)'''

        return recommendations
    except requests.RequestException as e:
        return [f"Error fetching exercises: {str(e)}"]

#def update_all_exercise()
def update_one_exercise(recommendations,exercise,muscle):
    """
    Delete an exercise, add a new exercise, and updating the recommendations

    Arg:
        recommendations: list of the recommended exercises
        exercise: string of the specific exercise the user want to update
        muscle: string of which muscle group the user wants to target

    Return:
        recommendations: the new updated list of recommended exercises
    """
    params = {
        "language": 2,  # default Language: English
        "api_key": API_KEY  
    }

    try:
        response = requests.get(f"{BASE_URL}exercise/", params=params)
        response.raise_for_status()
        data = response.json().get("results", []) # getting data
        
        for workouts in data:
            if muscle in workouts["description"].lower():
                index = recommendations.index(exercise)
                recommendations[index] = workouts["name"]
                break
        return recommendations
    except requests.RequestException as e:
        return [f"Error fetching exercises: {str(e)}"]



if __name__ == "__main__":
    try:
        print("\nPlease specify the muscle groups you'd like to target during your workout.")
        print("Please Choose one of the following: legs, biceps, back, abs, cardio")
        target_muscle_groups = input("Enter your preferred muscle groups, separated by commas: ").strip().lower()
        #for muscle in target_muscle_groups:
         #   if (muscle != "")

        muscle_groups_list = [muscle.strip() for muscle in target_muscle_groups.split(",")]

        print("\nFetching exercise recommendations...")
        exercises = fetch_exercise_by_muscle_group(muscle_groups_list)

        print(f"\nRecommended Exercises Targeting: {', '.join(muscle_groups_list)}")
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
                    exercise_to_update = input("\nEnter the name of the exercise you want to replace: ").strip()
                    muscle_group = input("Enter the muscle group you'd like the new exercise to target: ").strip().lower()

                    if exercise_to_update in exercises:
                        updated_recommendations = update_one_exercise(exercises, exercise_to_update, muscle_group)
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

