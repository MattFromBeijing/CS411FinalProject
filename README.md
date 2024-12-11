# Workout and Music Application

## Overview
The Workout and Music Application is tool to support individuals in achieving their fitness goals through tailored exercise recommendations, goal tracking, and comprehensive logging capabilities. It features seamless music integration, ensuring each workout is enriched with a fitting backtrack

## APIs Used
Wger Exercise API: https://wger.de/api/v2/exercisebaseinfo/

Jamendo Music API: https://api.jamendo.com/v3.0/tracks/

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

## Exercise Search

### Find Exercises by Target Groups

Route: /find-exercise-by-target-groups

Request Type: GET

Purpose: Finds exercises based on a user's target groups.

Query Parameters:

username: The username of the user.

Response Format: JSON

Success Response Example:

Code: 200

Content:

{ "status": "success", "exercises": ["<exercise1>", "<exercise2>"] }

## Logs Management

### Create Log

Route: /create-log

Request Type: POST

Purpose: Creates an exercise log for a user.

Request Body:

{
  "username": "<username>",
  "exercise_name": "<exercise_name>",
  "muscle_groups": ["<group1>", "<group2>"],
  "date": "<YYYY-MM-DD>"
}

Response Format: JSON

Success Response Example:

Code: 200

Content:

{ "status": "success" }

### Get All Logs

Route: /get-all-logs

Request Type: GET

Purpose: Retrieves all exercise logs for a user.

Query Parameters:

username: The username of the user.

Response Format: JSON

Success Response Example:

Code: 200

Content:

{ "status": "success", "exercises": ["<log1>", "<log2>"] }
