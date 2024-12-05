from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from workout.utils.sql_utils import check_database_connection, get_db_connection, check_table_exists
import sqlite3
import hashlib
import os

# from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# This bypasses standard security stuff we'll talk about later
# If you get errors that use words like cross origin or flight,
# uncomment this
# CORS(app)

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

