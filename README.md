# CS411FinalProject

Routes
1. Health Check
Route: /api/health
Request Type: GET
Purpose: Verifies that the service is running and healthy.

Request Body:
No parameters required.

Response Format:

Success Response Example:
Code: 200
Content: { "status": "healthy" }

Example Request:
curl -X GET http://localhost:5000/api/health

Example Response:

{
  "status": "healthy"
}


2. Create Account
Route: /api/create-account
Request Type: POST
Purpose: Creates a new user account with a username and password.

Request Body:

username (String): User's chosen username.
password (String): User's chosen password.

Response Format:

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

3. Login
Route: /api/login
Request Type: POST
Purpose: Verifies the username and password for a user login.

Request Body:

username (String): User's username.
password (String): User's password.

Response Format:

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

4. Update Password
Route: /api/update-password
Request Type: POST
Purpose: Updates the password for an existing user.

Request Body:

username (String): The username of the user.
new_password (String): The new password for the user.
Response Format:

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

5. Clear All Users
Route: /api/clear-users
Request Type: POST
Purpose: Clears all users from the database.

Request Body: No parameters required.

Response Format:

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
