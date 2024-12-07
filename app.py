from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from config import ProductionConfig, TestConfig
from workout.models.user_model import Users
from werkzeug.exceptions import BadRequest, Unauthorized

# Load environment variables from .env file
load_dotenv()

def create_app(config_class=TestConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

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

            Users.create_user(username, password)
            app.logger.info("User added: %s", username)
            return make_response(jsonify({'status': 'user added', 'username': username}), 201)
        except ValueError as e:
            return make_response(jsonify({'error': str(e)}), 400)
        except Exception as e:
            app.logger.error("Failed to add user: %s", str(e))
            return make_response(jsonify({'error': "An unexpected error occurred."}), 500)

    @app.route('/api/delete-user', methods=['DELETE'])
    def delete_user() -> Response:
        """
        Route to delete a user.

        Expected JSON Input:
            - username (str): The username of the user to be deleted.

        Returns:
            JSON response indicating the success of user deletion.
        """
        app.logger.info('Deleting user')
        try:
            data = request.get_json()
            username = data.get('username')

            if not username:
                raise BadRequest("The 'username' field is required.")

            Users.delete_user(username)
            app.logger.info("User deleted: %s", username)
            return make_response(jsonify({'status': 'user deleted', 'username': username}), 200)
        except ValueError as e:
            return make_response(jsonify({'error': str(e)}), 400)
        except Exception as e:
            app.logger.error("Failed to delete user: %s", str(e))
            return make_response(jsonify({'error': "An unexpected error occurred."}), 500)

    @app.route('/api/login', methods=['POST'])
    def login():
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

            if not Users.login(username, password):
                raise Unauthorized("Invalid username or password.")

            user_id = Users.get_id_by_username(username)
            app.logger.info("User %s logged in successfully.", username)
            return jsonify({"message": f"User {username} logged in successfully.", "user_id": user_id}), 200
        except Unauthorized as e:
            return jsonify({"error": str(e)}), 401
        except Exception as e:
            app.logger.error("Error during login for username %s: %s", username, str(e))
            return jsonify({"error": "An unexpected error occurred."}), 500

    @app.route('/api/update-password', methods=['POST'])
    def update_password():
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

            Users.update_password(username, new_password)
            return jsonify({"message": "Password updated successfully."}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred."}), 500

    # Ensure this is at the end
    return app
