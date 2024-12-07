#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

##############################################
#
# User management
#
##############################################

# Function to create a user
create_user() {
  echo "Creating a new user..."
  curl -s -X POST "$BASE_URL/create-account" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}' | grep -q '"status": "user added"'
  if [ $? -eq 0 ]; then
    echo "User created successfully."
  else
    echo "Failed to create user."
    exit 1
  fi
}

# Function to log in a user
login_user() {
  echo "Logging in user..."
  response=$(curl -s -X POST "$BASE_URL/login" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}')
  if echo "$response" | grep -q '"message": "User testuser logged in successfully."'; then
    echo "User logged in successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Login Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to log in user."
    exit 1
  fi
}

# Function to update user password
update_password() {
  echo "Updating password..."
  curl -s -X POST "$BASE_URL/update-password" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "new_password":"newpassword123"}' | grep -q '"message": "Password updated successfully."'
  if [ $? -eq 0 ]; then
    echo "Password updated successfully."
  else
    echo "Failed to update password."
    exit 1
  fi
}

# Function to delete a user
delete_user() {
  echo "Deleting user..."
  curl -s -X DELETE "$BASE_URL/delete-user" -H "Content-Type: application/json" \
    -d '{"username":"testuser"}' | grep -q '"status": "user deleted"'
  if [ $? -eq 0 ]; then
    echo "User deleted successfully."
  else
    echo "Failed to delete user."
    exit 1
  fi
}

# Function to clear all users
clear_all_users() {
  echo "Clearing all users..."
  curl -s -X POST "$BASE_URL/clear-users" | grep -q '"message": "All users cleared successfully."'
  if [ $? -eq 0 ]; then
    echo "All users cleared successfully."
  else
    echo "Failed to clear users."
    exit 1
  fi
}

###############################################
#
# Run smoketests
#
###############################################

check_health
create_user
login_user
update_password
delete_user
clear_all_users

echo "All smoketests passed successfully!"
