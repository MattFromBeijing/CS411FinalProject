# Workout and Music Application

## Overview
The Workout and Music Application is tool to support individuals in achieving their fitness goals through tailored exercise recommendations, goal tracking, and comprehensive logging capabilities. It features seamless music integration, ensuring each workout is enriched with a fitting backtrack

## Steps to Run the Application
1. Download all the files
2. Create the virtual environment in Linux Terminal using: source setup_venv.sh
3. Use the command sh run_docker.sh

  
## APIs Used
Wger Exercise API: https://wger.de/api/v2/exercisebaseinfo/
To use this API, go to the website https://wger.de/en/software/api
1. Create an account
2. Generate a key

Jamendo Music API: https://api.jamendo.com/v3.0/tracks/
To use this API, got to the website: https://developer.jamendo.com/v3.0
1. Create an account
2. Generate a key

## Features
### 1. Personalized Recommendations
Our Recommendations Model provides personalized exercise and music suggestions by managing user preferences such as target muscle groups, available equipment, and favorite songs. It integrates with external APIs to fetch tailored workout plans and playlists, ensuring a seamless and engaging user experience.
### 2. Workout Logging and Progress Tracking
Our app allows users to record details like:
*Exercise performed.
*Muscle groups targeted.
*Date and duration.
*Equipment used.
As well as retrieve historical workout logs for specific dates or targeted muscle groups.
We also allow users to delete their logs, as well as modify them
### 3. Equipment and Resources Management
Manage a list of available equipment to ensure workout recommendations align with user resources.
Update equipment availability dynamically to reflect changes in the user's environment.
### 4. Target Group Management
Users can set and update target muscle groups.
Retrieve exercises specifically curated for these target groups.
### 5. Music Integration
Access the Jamendo Music API to create playlists that enhance the workout experience.
Users can search for tracks based on mood, energy, or exercise type.
### 6. User Account Management
Create Account: Users can create personalized accounts.
Login: Secure authentication ensures user data privacy.
Update Password: Allows users to change their password for account security.
Clear Users: Admin functionality to reset all user data.


## Routes:
### Health Check
Route: /api/health

Request Type: GET

Purpose: Verifies that the service is running and healthy.

Request Body:
No parameters required.

Response Format: JSON

Success Response Example:
Code: 200
Content: { "status": "healthy" }

Example Request:
curl -X GET http://localhost:5000/api/health

Example Response:
{
  "status": "healthy"
}


### Create Account
Route: /api/create-account

Request Type: POST

Purpose: Creates a new user account with a username and password.

Request Body:

username (String): User's chosen username.
password (String): User's chosen password.

Response Format: JSON

Success Response Example:
Code: 201
Content: { "status": "user added", "username": "newuser123" }
Error Response Example:
Code: 400
Content: { "error": "Both 'username' and 'password' are required." }

Example Request:
curl -s -X POST "http://localhost:5000/api/create-account" -H "Content-Type: application/json" \
-d '{"username":"testuser", "password":"password123"}'

Example Response:
{
  "status": "user added",
  "username": "newuser123"
}

### Login
Route: /api/login

Request Type: POST

Purpose: Verifies the username and password for a user login.

Request Body:

username (String): User's username.
password (String): User's password.

Response Format: JSON

Success Response Example:
Code: 200
Content: { "message": "User newuser123 logged in successfully.", "user_id": 1 }
Error Response Example:
Code: 401
Content: { "error": "Invalid username or password." }

Example Request:
curl -s -X POST "http://localhost:5000/api/login" -H "Content-Type: application/json" \
-d '{"username":"testuser", "password":"password123"}'

Example Response:
{
  "message": "User newuser123 logged in successfully.",
  "user_id": 1
}

### Update Password
Route: /api/update-password

Request Type: POST

Purpose: Updates the password for an existing user.

Request Body:

username (String): The username of the user.
new_password (String): The new password for the user.

Response Format: JSON

Success Response Example:
Code: 200
Content: { "message": "Password updated successfully." }
Error Response Example:
Code: 400
Content: { "error": "Both 'username' and 'new_password' are required." }

Example Request:
curl -s -X POST "http://localhost:5000/api/update-password" -H "Content-Type: application/json" \
-d '{"username":"testuser", "new_password":"newpassword123"}'

Example Response:
{
  "message": "Password updated successfully."
}

### Clear All Users
Route: /api/clear-users

Request Type: POST

Purpose: Clears all users from the database.

Request Body: No parameters required.

Response Format: JSON

Success Response Example:
Code: 200
Content: { "message": "All users cleared successfully." }
Error Response Example:
Code: 500
Content: { "error": "An unexpected error occurred while clearing users." }

Example Request:
 curl -s -X POST "http://localhost:5000/api/clear-users"

Example Response:
{
  "message": "All users cleared successfully."
}

## Target Management

### Set Target Groups
Route: /api/set-target-groups

Request Type: POST

Purpose: Sets target groups for a specific user.

Request Body:

username (String): The username of the user.
groups (List[String]): A list of groups to set as targets.
Response Format: JSON

Success Response Example:
Code: 200
Content: { "status": "success" }

Error Response Examples:
Code: 400
Content: { "error": "username and groups required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X POST "http://localhost:5000/api/set-target-groups" -H "Content-Type: application/json" \
-d '{"username":"testuser", "groups":["group1", "group2"]}'

Example Response:
{
  "status": "success"
}

### Add Target Group
Route: /api/add-target-group

Request Type: POST

Purpose: Adds a single target group for a specific user.

Request Body:

username (String): The username of the user.
group (String): The group to be added as a target.
Response Format: JSON

Success Response Example:
Code: 200
Content: { "status": "success" }

Error Response Examples:
Code: 400
Content: { "error": "username and group required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X POST "http://localhost:5000/api/add-target-group" -H "Content-Type: application/json" \
-d '{"username":"testuser", "group":"group1"}'

Example Response:

{
  "status": "success"
}

### Remove Target Group
Route: /api/remove-target-group

Request Type: POST

Purpose: Removes a single target group from a specific user's targets.

Request Body:

username (String): The username of the user.
group (String): The group to be removed.
Response Format: JSON

Success Response Example:
Code: 200
Content: { "status": "success" }

Error Response Examples:
Code: 400
Content: { "error": "username and group required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X POST "http://localhost:5000/api/remove-target-group" -H "Content-Type: application/json" \
-d '{"username":"testuser", "group":"group1"}'

Example Response:

{
  "status": "success"
}

### Get Target Groups
Route: /api/get-target-groups

Request Type: GET

Purpose: Retrieves a list of target groups for a specific user.

Query Parameters:

username (String): The username of the user.
Response Format: JSON

Success Response Example:
Code: 200
Content:

{ 
  "status": "success", 
  "groups": ["group1", "group2"] 
}

Error Response Examples:
Code: 400
Content: { "error": "username required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X GET "http://localhost:5000/api/get-target-groups?username=testuser"

Example Response:

{
  "status": "success",
  "groups": ["group1", "group2"]
}

## Equiptment Management

### Set Available Equipment List
Route: /api/set-available-equipment-list

Request Type: POST

Purpose: Sets the available equipment list for a specific user.

Request Body:

username (String): The username of the user.
equipment_list (List[String]): A list of equipment to be set as available.
Response Format: JSON

Success Response Example:
Code: 200
Content: { "status": "success" }

Error Response Examples:
Code: 400
Content: { "error": "username and equipment_list required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X POST "http://localhost:5000/api/set-available-equipment-list" -H "Content-Type: application/json" \
-d '{"username":"testuser", "equipment_list":["item1", "item2"]}'

Example Response:

{
  "status": "success"
}

### Add Available Equipment
Route: /api/add-available-equipment

Request Type: POST

Purpose: Adds an item to the available equipment list for a specific user.

Request Body:

username (String): The username of the user.
equipment (String): The equipment item to be added to the user's list.
Response Format: JSON

Success Response Example:
Code: 200
Content: { "status": "success" }

Error Response Examples:
Code: 400
Content: { "error": "username and equipment required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X POST "http://localhost:5000/api/add-available-equipment" -H "Content-Type: application/json" \
-d '{"username":"testuser", "equipment":"item1"}'

Example Response:

{
  "status": "success"
}

### Remove Available Equipment
Route: /api/remove-available-equipment

Request Type: POST

Purpose: Removes an item from the available equipment list for a specific user.

Request Body:

username (String): The username of the user.
equipment (String): The equipment item to be removed from the user's list.
Response Format: JSON

Success Response Example:
Code: 200
Content: { "status": "success" }

Error Response Examples:
Code: 400
Content: { "error": "username and equipment required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X POST "http://localhost:5000/api/remove-available-equipment" -H "Content-Type: application/json" \
-d '{"username":"testuser", "equipment":"item1"}'

Example Response:

{
  "status": "success"
}

### Get Available Equipment
Route: /api/get-available-equipment

Request Type: GET

Purpose: Retrieves the available equipment list for a specific user.

Query Parameters:

username (String): The username of the user.
Response Format: JSON

Success Response Example:
Code: 200
Content:

{ 
  "status": "success", 
  "equipment_list": ["item1", "item2"] 
}

Error Response Examples:
Code: 400
Content: { "error": "username required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X GET "http://localhost:5000/api/get-available-equipment?username=testuser"

Example Response:

{
  "status": "success",
  "equipment_list": ["item1", "item2"]
}

## Finding Exercises (External API Calls)

### Find Exercises by Target Groups
Route: /api/find-exercise-by-target-groups

Request Type: GET

Purpose: Retrieves a list of exercises based on a user's target muscle groups.

Query Parameters:

username (String): The username of the user.
Response Format: JSON

Success Response Example:
Code: 200
Content:

{ 
  "status": "success", 
  "exercises": ["exercise1", "exercise2"] 
}

Error Response Examples:
Code: 400
Content: { "error": "username required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X GET "http://localhost:5000/api/find-exercise-by-target-groups?username=testuser"

Example Response:

{
  "status": "success",
  "exercises": ["exercise1", "exercise2"]
}

## Find Exercises by Groups
Route: /api/find-exercise-by-groups

Request Type: GET

Purpose: Retrieves a list of exercises based on specified muscle groups.

Query Parameters:

username (String): The username of the user.
groups (List[String]): A list of muscle groups to search for exercises.
Response Format: JSON

Success Response Example:
Code: 200
Content:

{ 
  "status": "success", 
  "exercises": ["exercise1", "exercise2"] 
}

Error Response Examples:
Code: 400
Content: { "error": "username and groups required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X GET "http://localhost:5000/api/find-exercise-by-groups?username=testuser&groups=arms&groups=legs"

Example Response:

{
  "status": "success",
  "exercises": ["exercise1", "exercise2"]
}

### Find Exercises by Available Equipment
Route: /api/find-exercise-by-available-equipment

Request Type: GET

Purpose: Retrieves a list of exercises based on the user's available equipment.

Query Parameters:

username (String): The username of the user.
Response Format: JSON

Success Response Example:
Code: 200
Content:

{ 
  "status": "success", 
  "exercises": ["exercise1", "exercise2"] 
}

Error Response Examples:
Code: 400
Content: { "error": "username required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X GET "http://localhost:5000/api/find-exercise-by-available-equipment?username=testuser"

Example Response:

{
  "status": "success",
  "exercises": ["exercise1", "exercise2"]
}

## Find Exercises by Specified Equipment
Route: /api/find-exercise-by-equipment

Request Type: GET

Purpose: Retrieves a list of exercises based on specified equipment.

Query Parameters:

username (String): The username of the user.
equipment (List[String]): A list of equipment items to search for exercises.
Response Format: JSON

Success Response Example:
Code: 200
Content:

{ 
  "status": "success", 
  "exercises": ["exercise1", "exercise2"] 
}

Error Response Examples:
Code: 400
Content: { "error": "username and equipment required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X GET "http://localhost:5000/api/find-exercise-by-equipment?username=testuser&equipment=dumbbells&equipment=bench"

Example Response:

{
  "status": "success",
  "exercises": ["exercise1", "exercise2"]
}


## Logs Management
### Create Log
Route: /api/create-log

Request Type: POST

Purpose: Creates an exercise log for a specific user.

Request Body:

username (String): The username of the user.
exercise_name (String): The name of the exercise.
muscle_groups (List[String]): A list of muscle groups targeted by the exercise.
date (String): The date of the exercise log (in a valid date format).
Response Format: JSON

Success Response Example:
Code: 200
Content: { "status": "success" }

Error Response Examples:
Code: 400
Content: { "error": "username, exercise_name, muscle_groups, and date required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X POST "http://localhost:5000/api/create-log" -H "Content-Type: application/json" \
-d '{"username":"testuser", "exercise_name":"squat", "muscle_groups":["legs"], "date":"2024-12-10"}'
Example Response:

{
  "status": "success"
}

### Clear Logs
Route: /api/clear-logs

Request Type: POST

Purpose: Clears all exercise logs for a specific user.

Request Body:

username (String): The username of the user.
Response Format: JSON

Success Response Example:
Code: 200
Content: { "status": "success" }

Error Response Examples:
Code: 400
Content: { "error": "username required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X POST "http://localhost:5000/api/clear-logs" -H "Content-Type: application/json" \
-d '{"username":"testuser"}'

Example Response:

{
  "status": "success"
}

### Delete Log by Date
Route: /api/delete-log-by-date

Request Type: POST

Purpose: Deletes an exercise log for a specific user based on the date.

Request Body:

username (String): The username of the user.
date (String): The date of the log to delete (in a valid date format).
Response Format: JSON

Success Response Example:
Code: 200
Content: { "status": "success" }

Error Response Examples:
Code: 400
Content: { "error": "username and date required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X POST "http://localhost:5000/api/delete-log-by-date" -H "Content-Type: application/json" \
-d '{"username":"testuser", "date":"2024-12-10"}'
Example Response:

{
  "status": "success"
}

### Get All Logs
Route: /api/get-all-logs

Request Type: GET

Purpose: Retrieves all exercise logs for a specific user.

Query Parameters:

username (String): The username of the user.
Response Format: JSON

Success Response Example:
Code: 200
Content:

{ 
  "status": "success", 
  "exercises": [
    { "exercise_name": "squat", "muscle_groups": ["legs"], "date": "2024-12-10" }
  ] 
}
Error Response Examples:
Code: 400
Content: { "error": "username required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X GET "http://localhost:5000/api/get-all-logs?username=testuser"

Example Response:

{
  "status": "success",
  "exercises": [
    { "exercise_name": "squat", "muscle_groups": ["legs"], "date": "2024-12-10" }
  ]
}

### Get Log by Date
Route: /api/get-log-by-date

Request Type: GET

Purpose: Retrieves exercise logs for a specific date for a user.

Query Parameters:

username (String): The username of the user.
date (String): The date of the logs to retrieve (in a valid date format).
Response Format: JSON

Success Response Example:
Code: 200
Content:

{ 
  "status": "success", 
  "exercises": [
    { "exercise_name": "squat", "muscle_groups": ["legs"], "date": "2024-12-10" }
  ] 
}
Error Response Examples:
Code: 400
Content: { "error": "username and date required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X GET "http://localhost:5000/api/get-log-by-date?username=testuser&date=2024-12-10"

Example Response:

{
  "status": "success",
  "exercises": [
    { "exercise_name": "squat", "muscle_groups": ["legs"], "date": "2024-12-10" }
  ]
}

### Get Logs by Muscle Group
Route: /api/get-log-by-muscle-group

Request Type: GET

Purpose: Retrieves exercise logs for a specific muscle group for a user.

Query Parameters:

username (String): The username of the user.
muscle_group (String): The muscle group for which to retrieve logs.
Response Format: JSON

Success Response Example:
Code: 200
Content:

{ 
  "status": "success", 
  "exercises": [
    { "exercise_name": "squat", "muscle_groups": ["legs"], "date": "2024-12-10" }
  ] 
}

Error Response Examples:
Code: 400
Content: { "error": "username and muscle_group required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X GET "http://localhost:5000/api/get-log-by-muscle-group?username=testuser&muscle_group=legs"
Example Response:

{
  "status": "success",
  "exercises": [
    { "exercise_name": "squat", "muscle_groups": ["legs"], "date": "2024-12-10" }
  ]
}

### Update Log
Route: /api/update-log

Request Type: POST

Purpose: Updates an exercise log for a specific user.

Request Body:

username (String): The username of the user.
exercise_name (String): The name of the exercise to update.
muscle_groups (List[String]): A list of muscle groups targeted by the exercise.
date (String): The date of the log to update (in a valid date format).
Response Format: JSON

Success Response Example:
Code: 200
Content: { "status": "success" }

Error Response Examples:
Code: 400
Content: { "error": "username, exercise_name, muscle_groups, and date required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X POST "http://localhost:5000/api/update-log" -H "Content-Type: application/json" \
-d '{"username":"testuser", "exercise_name":"squat", "muscle_groups":["legs"], "date":"2024-12-10"}'

Example Response:

{
  "status": "success"
}

## Song Management
### Fetch Songs by Workouts
Route: /api/fetch-songs-by-workouts

Request Type: GET

Purpose: Fetches a list of songs based on the number of workouts completed by the user.

Query Parameters:

username (String): The username of the user.
workout_count (Integer, optional): The number of workouts completed by the user. Defaults to 1 if not provided.
Response Format: JSON

Success Response Example:
Code: 200
Content:

{
  "status": "success",
  "songs": [
    { "name": "Song 1", "artist": "Artist 1" },
    { "name": "Song 2", "artist": "Artist 2" }
  ]
}

Error Response Examples:
Code: 400
Content: { "error": "username required" }

Code: 404
Content: { "error": "username not found" }

Code: 404
Content: { "status": "error", "songs": "no songs found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X GET "http://localhost:5000/api/fetch-songs-by-workouts?username=testuser&workout_count=5"

Example Response:

{
  "status": "success",
  "songs": [
    { "name": "Song 1", "artist": "Artist 1" },
    { "name": "Song 2", "artist": "Artist 2" }
  ]
}

### Fetch Random Song
Route: /api/fetch-random-song

Request Type: GET

Purpose: Fetches a random song using the Jamendo API.

Query Parameters:

username (String): The username of the user.
Response Format: JSON

Success Response Example:
Code: 200
Content:

{
  "status": "success",
  "song": { "name": "Random Song", "artist": "Random Artist" }
}

Error Response Examples:
Code: 400
Content: { "error": "username required" }

Code: 404
Content: { "error": "username not found" }

Code: 500
Content: { "error": "An unexpected error occurred." }

Example Request:

curl -s -X GET "http://localhost:5000/api/fetch-random-song?username=testuser"

Example Response:

{
  "status": "success",
  "song": { "name": "Random Song", "artist": "Random Artist" }
}
