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
  username=$1
  password=$2
  echo "Creating a new user: $username..."
  curl -s -X POST "$BASE_URL/create-account" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"password\":\"$password\"}" | grep -q '"status": "user added"'
  if [ $? -eq 0 ]; then
    echo "User created successfully."
  else
    echo "Failed to create user."
    exit 1
  fi
}



# Function to log in a user
login_user() {
  username=$1
  password=$2
  echo "Logging in user: $username..."
  response=$(curl -s -X POST "$BASE_URL/login" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"password\":\"$password\"}")
  if echo "$response" | grep -q '"message": "User '"$username"' logged in successfully."'; then
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
  username=$1
  new_password=$2
  echo "Updating password for user: $username..."
  curl -s -X POST "$BASE_URL/update-password" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"new_password\":\"$new_password\"}" | grep -q '"message": "Password updated successfully."'
  if [ $? -eq 0 ]; then
    echo "Password updated successfully."
  else
    echo "Failed to update password."
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
# Target Management
#
###############################################

set_target_groups() {
  username=$1
  groups=$2
  echo "Setting target groups for $username..."
  curl -s -X POST "$BASE_URL/set-target-groups" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"groups\":$groups}" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Target groups set successfully."
  else
    echo "Failed to set target groups."
    exit 1
  fi
}

add_target_group() {
  username=$1
  group=$2
  echo "Adding target group $group for $username..."
  curl -s -X POST "$BASE_URL/add-target-group" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"group\":\"$group\"}" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Target group added successfully."
  else
    echo "Failed to add target group."
    exit 1
  fi
}

remove_target_group() {
  username=$1
  group=$2
  echo "Removing target group $group for $username..."
  curl -s -X POST "$BASE_URL/remove-target-group" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"group\":\"$group\"}" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Target group removed successfully."
  else
    echo "Failed to remove target group."
    exit 1
  fi
}

get_target_groups() {
  username=$1
  echo "Fetching target groups for user: $username..."
  response=$(curl -s -X GET "$BASE_URL/get-target-groups?username=$username")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Target groups fetched successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to fetch target groups."
    echo "$response"
    exit 1
  fi
}

###############################################
#
# Equipment Management
#
###############################################

set_equipment_list() {
  username=$1
  equipment_list=$2
  echo "Setting equipment list for $username..."
  curl -s -X POST "$BASE_URL/set-available-equipment-list" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"equipment_list\":$equipment_list}" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Equipment list set successfully."
  else
    echo "Failed to set equipment list."
    exit 1
  fi
}

add_equipment() {
  username=$1
  equipment=$2
  echo "Adding equipment $equipment for $username..."
  curl -s -X POST "$BASE_URL/add-available-equipment" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"equipment\":\"$equipment\"}" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Equipment added successfully."
  else
    echo "Failed to add equipment."
    exit 1
  fi
}

remove_equipment() {
  username=$1
  equipment=$2
  echo "Removing equipment $equipment for $username..."
  curl -s -X POST "$BASE_URL/remove-available-equipment" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"equipment\":\"$equipment\"}" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Equipment removed successfully."
  else
    echo "Failed to remove equipment."
    exit 1
  fi
}

get_available_equipment() {
  username=$1
  echo "Fetching available equipment for user: $username..."
  response=$(curl -s -X GET "$BASE_URL/get-available-equipment?username=$username")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Available equipment fetched successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to fetch available equipment."
    echo "$response"
    exit 1
  fi
}

###############################################
#
# Finding Exercises (external API calls)
#
###############################################

find_exercise_by_target_groups() {
  username=$1
  echo "Finding exercises by target groups for user: $username..."
  response=$(curl -s -X GET "$BASE_URL/find-exercise_by-target_groups?username=$username")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Exercises found by target groups successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to find exercises by target groups."
    echo "$response"
    exit 1
  fi
}

find_exercise_by_groups() {
  username=$1
  groups=$2

  groups_query=$(echo "$groups" | jq -r '.[]' | awk '{print "&groups=" $0}' | tr -d '\n')

  echo "Finding exercises by groups for user: $username..."
  response=$(curl -s -X GET "$BASE_URL/find-exercise-by-groups?username=$username$groups_query")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Exercises found by groups successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to find exercises by groups."
    echo "$response"
    exit 1
  fi
}

find_exercise_by_available_equipment() {
  username=$1
  echo "Finding exercises by available equipment for user: $username..."
  response=$(curl -s -X GET "$BASE_URL/find-exercise-by-available-equipment?username=$username")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Exercises found by available equipment successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to find exercises by available equipment."
    echo "$response"
    exit 1
  fi
}

find_exercise_by_equipment() {
  username=$1
  equipment=$2

  equipment_query=$(echo "$groups" | jq -r '.[]' | awk '{print "&equipment=" $0}' | tr -d '\n')

  echo "Finding exercises by specific equipment for user: $username..."
  response=$(curl -s -X GET "$BASE_URL/find-exercise-by-available-equipment?username=$username$equipment_query")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Exercises found by specific equipment successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to find exercises by specific equipment."
    echo "$response"
    exit 1
  fi
}

###############################################
#
# Log Management
#
###############################################

create_log() {
  username=$1
  exercise_name=$2
  muscle_groups=$3
  date=$4
  echo "Creating a log for user: $username..."
  response=$(curl -s -X POST "$BASE_URL/create-log" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"exercise_name\":\"$exercise_name\", \"muscle_groups\":\"$muscle_groups\", \"date\":\"$date\"}")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Log created successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to create log."
    echo "$response"
    exit 1
  fi
}

clear_logs() {
  username=$1
  echo "Clearing all logs for user: $username..."
  response=$(curl -s -X POST "$BASE_URL/clear-logs" -H "Content-Type: application/json" -d "{\"username\":\"$username\"}")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Logs cleared successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to clear logs."
    echo "$response"
    exit 1
  fi
}

delete_log_by_date() {
  username=$1
  date=$2
  echo "Delete $date log for user: $username..."
  response=$(curl -s -X POST "$BASE_URL/delete-log-by-date" -H "Content-Type: application/json" -d "{\"username\":\"$username\", \"date\":\"$date\"}")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Logs cleared successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to clear logs."
    echo "$response"
    exit 1
  fi
}

get_all_logs() {
  username=$1
  echo "Fetching all logs for user: $username..."
  response=$(curl -s -X GET "$BASE_URL/get-all-logs?username=$username")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Fetched all logs successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to fetch logs."
    echo "$response"
    exit 1
  fi
}

get_log_by_date() {
  username=$1
  date=$2
  echo "Fetching logs for user: $username on date: $date..."
  response=$(curl -s -X GET "$BASE_URL/get-log-by-date?username=$username&date=$date")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Fetched logs by date successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to fetch logs by date."
    echo "$response"
    exit 1
  fi
}

update_log() {
  username=$1
  exercise_name=$2
  muscle_groups=$3
  date=$4
  echo "Updating log for user: $username..."
  response=$(curl -s -X POST "$BASE_URL/update-log" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"exercise_name\":\"$exercise_name\", \"muscle_groups\":\"$muscle_groups\", \"date\":\"$date\"}")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Log updated successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to update log."
    echo "$response"
    exit 1
  fi
}

###############################################
#
# Run smoketests
#
###############################################

check_health
clear_all_users

create_user "testuser1" "password123"
login_user "testuser1" "password123"
update_password "testuser1" "newpassword123"
clear_all_users

create_user "testuser1" "password123"
login_user "testuser1" "password123"

set_target_groups "testuser1" '["leg", "arm"]'
add_target_group "testuser1" "back"
remove_target_group "testuser1" "back"
get_target_groups "testuser1"

find_exercise_by_target_groups "testuser1"
find_exercise_by_groups "testuser1" '["leg", "arm"]'

set_equipment_list "testuser1" '["dumbbell"]'
add_equipment "testuser1" "kettlebell"
remove_equipment "testuser1" "kettlebell"
get_available_equipment "testuser1"

find_exercise_by_available_equipment "testuser1"
find_exercise_by_equipment "testuser1" '["dumbbell"]'

create_user "testuser2" "password123"
login_user "testuser2" "password123"
create_log "testuser2" "Bench Press" "arm" "2024-12-10"

create_log "testuser1" "Bench Press" "arm" "2024-12-10"
create_log "testuser1" "Leg Press" "leg" "2024-12-11"
get_all_logs "testuser1"
get_log_by_date "testuser1" "2024-12-10"
update_log "testuser1" "Swim" "cardio" "2024-12-10"
clear_logs "testuser1"

get_all_logs "testuser2"
delete_log_by_date "testuser2" "2024-12-10"

echo "All smoketests passed successfully!"