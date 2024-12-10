from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from config import ProductionConfig, TestConfig
from werkzeug.exceptions import BadRequest, Unauthorized
import logging

from typing import Dict
from workout.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

from workout.models.user_model import create_user, login, update_password, clear_users, get_id_by_username
from workout.models.recommendations_model import RecommendationsModel, Exercise
from workout.models.log_model import *

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

accounts: Dict[str, RecommendationsModel] = {}

####################################################
#
# Healthchecks
#
####################################################

@app.route('/api/health', methods=['GET'])
def healthcheck() -> Response:
    """
    Health check route to verify the service is running.

    Returns:
        JSON response indicating the health status of the service.
    """
    app.logger.info('Health check')
    return make_response(jsonify({'status': 'healthy'}), 200)

##########################################################
#
# User Management
#
##########################################################

@app.route('/api/create-account', methods=['POST'])
def create_account() -> Response:
    """
    Route to create a new user.

    Expected JSON Input:
        - username (str): The username for the new user.
        - password (str): The password for the new user.

    Returns:
        JSON response indicating the success of user creation.
    """
    app.logger.info('Creating new user')
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise BadRequest("Both 'username' and 'password' are required.")

        create_user(username, password)
        accounts[username] = RecommendationsModel(username)
        app.logger.info("User added: %s", username)
        
        return make_response(jsonify({'status': 'user added', 'username': username}), 201)
    except ValueError as e:
        return make_response(jsonify({'error': str(e)}), 400)
    except Exception as e:
        app.logger.error("Failed to add user: %s", str(e))
        return make_response(jsonify({'error': "An unexpected error occurred."}), 500)

@app.route('/api/login', methods=['POST'])
def user_login():
    """
    Route to log in a user.

    Expected JSON Input:
        - username (str): The username of the user.
        - password (str): The user's password.

    Returns:
        JSON response indicating the success of the login.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise BadRequest("Both 'username' and 'password' are required.")

        if not login(username, password):
            raise Unauthorized("Invalid username or password.")

        user_id = get_id_by_username(username)
        app.logger.info("User %s logged in successfully.", username)
        return jsonify({"message": f"User {username} logged in successfully.", "user_id": user_id}), 200
    except Unauthorized as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        app.logger.error("Error during login for username %s: %s", username, str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/api/update-password', methods=['POST'])
def update_user_password():
    """
    Route to update a user's password.

    Expected JSON Input:
        - username (str): The username of the user.
        - new_password (str): The new password for the user.

    Returns:
        JSON response indicating the success of the password update.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        new_password = data.get('new_password')

        if not username or not new_password:
            raise BadRequest("Both 'username' and 'new_password' are required.")

        update_password(username, new_password)
        app.logger.info("Password updated successfully for user: %s", username)
        return jsonify({"message": "Password updated successfully."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error("Error updating password for username %s: %s", username, str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/api/clear-users', methods=['POST'])
def clear_users_route():
    """
    Route to clear all users from the login table.

    This recreates the login table, effectively deleting all users.

    Returns:
        JSON response indicating the success of the operation.
    """
    app.logger.warning("Attempting to clear all users. Ensure this route is secure.")
    try:
        clear_users()
        accounts.clear()
        app.logger.info("All users cleared successfully.")
        return jsonify({"message": "All users cleared successfully."}), 200
    except Exception as e:
        app.logger.error("Error clearing users: %s", str(e))
        return jsonify({"error": "An unexpected error occurred while clearing users."}), 500
    
##########################################################
#
# Target Management
#
##########################################################
    
@app.route('/api/set-target-groups', methods=['POST'])
def api_set_target_groups():
    """
    Route to set target groups for a user.

    Expected JSON Input:
        - username (str): The username of the user.
        - groups (list): A list of groups to set as targets.

    Returns:
        JSON response indicating the success or failure of the operation.
    """    
    try:
        data = request.get_json()
        username = data.get('username')
        groups = data.get('groups')
        
        if not username or not groups: return jsonify({"error": "username and groups required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}, 404)
        
        model = accounts[username]
        result = model.set_target_groups(groups)
        
        if result:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error"}), 500
        
    except Exception as e:
        app.logger.info(e)
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route('/api/add-target-group', methods=['POST'])
def api_add_target_group():
    """
    Route to add one target group for a user.

    Expected JSON Input:
        - username (str): The username of the user.
        - group (str): The group to be added as a target.

    Returns:
        JSON response indicating the success or failure of the operation.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        group = data.get('group')
        
        if not username or not group: return jsonify({"error": "username and group required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        model = accounts[username]
        result = model.add_target_group(group)
        
        if result:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error"}), 500
        
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/remove-target-group', methods=['POST'])
def api_remove_target_group():
    """
    Route to remove a target group for a user.

    Expected JSON Input:
        - username (str): The username of the user.
        - group (str): The group to be removed from the user's targets.

    Returns:
        JSON response indicating the success or failure of the operation.
    """
    try: 
        data = request.get_json()
        username = data.get('username')
        group = data.get('group')
        
        if not username or not group: return jsonify({"error": "username and group required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        model = accounts[username]
        result = model.remove_target_group(group)
        
        if result:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error"}), 500
        
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/get-target-groups', methods=['GET'])
def api_get_target_groups():
    """
    Route to retrieve target groups for a user.

    Query Parameters:
        - username (str): The username of the user.

    Returns:
        JSON response containing the status of the operation and a list of the user's target groups.
    """
    try:
        username = request.args.get('username')
        
        if not username: return jsonify({"error": "username required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        model = accounts[username]
        groups = model.get_target_groups()
        
        return jsonify({"status": "success", "groups": groups}), 200
        
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500
    
##########################################################
#
# Equipment Management
#
##########################################################

@app.route('/api/set-available-equipment-list', methods=['POST'])
def api_set_available_equipment_list():
    """
    Route to set the available equipment list for a user.

    Expected JSON Input:
        - username (str): The username of the user.
        - equipment_list (list): A list of equipment to be set as available.

    Returns:
        JSON response indicating the success or failure of the operation.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        equipment_list = data.get('equipment_list')
        
        if not username or not equipment_list: return jsonify({"error": "username and equipment_list required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        model = accounts[username]
        result = model.set_equipment(equipment_list)
        
        if result:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error"}), 500
        
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/add-available-equipment', methods=['POST'])
def api_add_available_equipment():
    """
    Route to add an item to the available equipment list for a user.

    Expected JSON Input:
        - username (str): The username of the user.
        - equipment (str): The equipment item to be added to the user's list.

    Returns:
        JSON response indicating the success or failure of the operation.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        equipment = data.get('equipment')
        
        if not username or not equipment: return jsonify({"error": "username and equipment required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        model = accounts[username]
        result = model.add_equipment(equipment)
        
        if result:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error"}), 500
        
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/remove-available-equipment', methods=['POST'])
def api_remove_available_equipment():
    """
    Route to remove an item from the available equipment list for a user.

    Expected JSON Input:
        - username (str): The username of the user.
        - equipment (str): The equipment item to be removed from the user's list.

    Returns:
        JSON response indicating the success or failure of the operation.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        equipment = data.get('equipment')
        
        if not username or not equipment: return jsonify({"error": "username and equipment required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        model = accounts[username]
        result = model.remove_equipment(equipment)
        
        if result:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error"}), 500
        
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/get-available-equipment', methods=['GET'])
def api_get_available_equipment():
    """
    Route to retrieve the available equipment list for a user.

    Query Parameters:
        - username (str): The username of the user.

    Returns:
        JSON response containing the status of the operation and the user's available equipment list.
    """
    try:
        username = request.args.get('username')
        
        if not username: return jsonify({"error": "username required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        model = accounts[username]
        equipment = model.get_equipment()
        
        return jsonify({"status": "success", "equipment": equipment}), 200
        
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500
    
##########################################################
#
# Finding Exercises (external API calls)
#
##########################################################

@app.route('/api/find-exercise_by-target_groups', methods=['GET'])
def api_find_exercise_by_target_groups():
    """
    Route to find exercises based on a user's target muscle groups.

    Query Parameters:
        - username (str): The username of the user.

    Returns:
        JSON response containing the status of the operation and a list of exercises matching the user's target groups.
    """
    try:
        username = request.args.get('username')
        
        if not username: return jsonify({"error": "username required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        model = accounts[username]
        target_groups = model.get_target_groups()
        exercises = model.get_exercises_by_many_muscle_groups(target_groups)
        
        return jsonify({"status": "success", "exercises": exercises}), 200
        
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/find-exercise-by-groups', methods=['GET'])
def api_find_exercise_by_groups():
    """
    Route to find exercises based on specified muscle groups.

    Query Parameters:
        - username (str): The username of the user.
        - groups (list): A list of muscle groups to search for exercises.

    Returns:
        JSON response containing the status of the operation and a list of exercises matching the specified muscle groups.
    """
    try:
        username = request.args.get('username')
        groups = request.args.getlist('groups')

        if not username or not groups: return jsonify({"error": "username and groups required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        model = accounts[username]
        exercises = model.get_exercises_by_many_muscle_groups(groups)
        
        return jsonify({"status": "success", "exercises": exercises}), 200
        
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/find-exercise-by-available-equipment', methods=['GET'])
def api_find_exercise_by_available_equipment():
    """
    Route to find exercises based on the user's available equipment.

    Query Parameters:
        - username (str): The username of the user.

    Returns:
        JSON response containing the status of the operation and a list of exercises that can be performed with the available equipment.
    """
    try:
        username = request.args.get('username')

        if not username: return jsonify({"error": "username required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        model = accounts[username]
        available_equipment = model.get_equipment()
        exercises = model.get_exercises_by_many_equipment(available_equipment)
        
        return jsonify({"status": "success", "exercises": exercises}), 200
        
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/find-exercise-by-available-equipment', methods=['GET'])
def api_find_exercise_by_equipment():
    """
    Route to find exercises based on specified equipment.

    Query Parameters:
        - username (str): The username of the user.
        - equipment (list): A list of equipment items to search for exercises.

    Returns:
        JSON response containing the status of the operation and a list of exercises that can be performed with the specified equipment.
    """
    try:
        data = request.get_json()
        username = data.request.args.get('username')
        equipment = data.request.args.getlist('equipment')

        if not username or not equipment: return jsonify({"error": "username and equipment required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        model = accounts[username]
        exercises = model.get_exercises_by_many_equipment(equipment)
        
        return jsonify({"status": "success", "exercises": exercises}), 200

    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500
    
##########################################################
#
# Log Management
#
##########################################################
    
@app.route('/api/create-log', methods=['POST'])
def api_create_log():
    """
    Route to create an exercise log for a user.

    Expected JSON Input:
        - username (str): The username of the user.
        - exercise_name (str): The name of the exercise.
        - muscle_groups (list): A list of muscle groups targeted by the exercise.
        - date (str): The date of the exercise log (in a valid date format).

    Returns:
        JSON response indicating the success or failure of the operation.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        exercise_name = data.get('exercise_name')
        muscle_groups = data.get('muscle_groups')
        date = data.get('date')
        
        if not (username and exercise_name and muscle_groups and date): return jsonify({"error": "username, exercise_name, muscle_groups, and date required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        result = create_log(username, exercise_name, muscle_groups, date)
        if result:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error"}), 500
        
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/clear-logs', methods=['POST'])
def api_clear_logs():
    try:
        data = request.get_json()
        username = data.get('username')
        
        if not username: return jsonify({"error": "username required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        result = clear_logs(username)
        if result:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error"}), 500
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/delete-log-by-date', methods=['POST'])
def api_delete_log_by_date():
    """
    Route to clear all exercise logs for a user.

    Expected JSON Input:
        - username (str): The username of the user.

    Returns:
        JSON response indicating the success or failure of the operation.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        date = data.get('date')
        
        if not username or not date: return jsonify({"error": "username and date required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        result = delete_log_by_date(username, date)
        if result:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error"}), 500
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/get-all-logs', methods=['GET'])
def api_get_all_logs():
    """
    Route to retrieve all exercise logs for a user.

    Query Parameters:
        - username (str): The username of the user.

    Returns:
        JSON response containing the status of the operation and a list of all exercise logs for the user.
    """
    try:
        username = request.args.get('username')
        
        if not username: return jsonify({"error": "username required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        result = get_all_logs(username)
        
        return jsonify({"status": "success", "exercises": result}), 200
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/get-log-by-date', methods=['GET'])
def api_get_log_by_date():
    """
    Route to retrieve exercise logs for a specific date for a user.

    Query Parameters:
        - username (str): The username of the user.
        - date (str): The date of the logs to retrieve (in a valid date format).

    Returns:
        JSON response containing the status of the operation and a list of exercises logged for the specified date.
    """
    try:
        username = request.args.get('username')
        date = request.args.get('date')
        
        if not username or not date: return jsonify({"error": "username and date required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        result = get_log_by_date(username, date)
        
        return jsonify({"status": "success", "exercises": result}), 200
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/get-log-by-muscle-group', methods=['GET'])
def api_get_logs_by_muscle_group():
    """
    Route to retrieve exercise logs for a specific muscle group for a user.

    Query Parameters:
        - username (str): The username of the user.
        - muscle_group (str): The muscle group for which to retrieve logs.

    Returns:
        JSON response containing the status of the operation and a list of exercises targeting the specified muscle group.
    """
    try:
        username = request.args.get('username')
        muscle_group = request.args.get('muscle_group')
        
        if not username or not muscle_group: return jsonify({"error": "username and muscle_group required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        result = get_logs_by_muscle_group(username, muscle_group)
        
        return jsonify({"status": "success", "exercises": result}), 200
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/update-log', methods=['POST'])
def api_update_log():
    """
    Route to update an exercise log for a user.

    Expected JSON Input:
        - username (str): The username of the user.
        - exercise_name (str): The name of the exercise to be updated.
        - muscle_groups (list): A list of muscle groups targeted by the exercise.
        - date (str): The date of the log to be updated (in a valid date format).

    Returns:
        JSON response indicating the success or failure of the update operation.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        exercise_name = data.get('exercise_name')
        muscle_groups = data.get('muscle_groups')
        date = data.get('date')
        
        if not (username and exercise_name and muscle_groups and date): return jsonify({"error": "username, exercise_name, muscle_groups, and date required"}), 400
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        if username not in accounts: return jsonify({"error": "username not found"}), 404
        
        result = update_log(username, date, exercise_name, muscle_groups)
        if result:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error"}), 500
    except Exception as e:
        app.logger.info(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)