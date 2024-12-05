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
    params = {"language": 2}  # Language: English

    try:
        response = requests.get(f"{BASE_URL}exercise/", params=params)
        response.raise_for_status()
        data = response.json().get("results", []) # getting data

        # Recommendation logic based on weight difference, lose or gain weight or maintain
        recommendations = []
        weight_difference = current_weight - desired_weight

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

# Example usage
if __name__ == "__main__":
    # Get user input
    current_weight = float(input("Enter your current weight (in pounds): "))
    desired_weight = float(input("Enter your desired weight (in pounds): "))

    # Fetch exercises for the user's current and desired weights
    exercises = fetch_exercises_by_weights(current_weight, desired_weight)

    # Display results
    print(f"\nYour current weight: {current_weight} lb")
    print(f"Your desired weight: {desired_weight} lb")
    print("\nRecommended Exercises Based on Your Goal:")
    for exercise in exercises:
        print(f"- {exercise}")
