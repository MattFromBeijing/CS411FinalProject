import requests

# Base URL for the wger API
BASE_URL = "https://wger.de/api/v2/"

def fetch_exercises_by_weights(current_weight, desired_weight):
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
        return [f"Error fetching exercises: {str(e)}"]

def fetch_exercise_by_muscle_group(list_of_muscle_group,target_time):
    """
    Fetch exercises based on the user's target muscle groups. Recommend exercises based on time constraint and target muscle

    Arg:
        list_of_muscle_group: list of target muscle from user
        target_time: integer of user's target workout time

    Return:
        recommendations: list of recommended exercises
    """
    params = {"language": 2}  # default Language: English

    try:
        response = requests.get(f"{BASE_URL}exercise/", params=params)
        response.raise_for_status()
        data = response.json().get("results", []) # getting data

        # Recommendation logic based on time and target muscle
        recommendations = []
        minutes_per_muscle = target_time // len(list_of_muscle_group) # dividing the time based on the number of targetted muscles
        if exercise in data: 
            for muscle in list_of_muscle_group: 
                while(minutes_per_muscle>=0): # time constraint
                    if muscle in exercise["description"].lower():
                        recommendations.append(exercise["name"])
                        minutes_per_muscle -= 3 # setting it to 3 mins per exercise for now
                minutes_per_muscle = target_time // len(list_of_muscle_group) # reset the time
        return recommendations
    except requests.RequestException as e:
        return [f"Error fetching exercises: {str(e)}"]

#def update_all_exercise()
def update_one_exercise(recommendations,exercise):
    """
    Delete an exercise, add a new exercise, and updating the recommendations

    Arg:
        recommendations: list of the recommended exercises
        exercise: string of the specific exercise the user want to update

    Return:
        recommendations: the new updated list of recommended exercises
    """
    params = {"language": 2}  # default Language: English

    try:
        response = requests.get(f"{BASE_URL}exercise/", params=params)
        response.raise_for_status()
        data = response.json().get("results", []) # getting data

    except requests.RequestException as e:
        return [f"Error fetching exercises: {str(e)}"]



if __name__ == "__main__":
    # Get user input - their weight
    current_weight = float(input("Enter your current weight (in pounds): "))
    desired_weight = float(input("Enter your desired weight (in pounds): "))

    # Fetch exercise recommendations for the user's current and desired weights
    exercises = fetch_exercises_by_weights(current_weight, desired_weight)

    print(f"\nYour current weight: {current_weight} lb")
    print(f"Your desired weight: {desired_weight} lb")
    print("\nRecommended Exercises Based on Your Goal:")
    for exercise in exercises:
        print(f"- {exercise}")
