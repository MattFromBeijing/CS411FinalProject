import pytest
from flask import Flask
from app import create_app  # Assuming the provided code is saved in `app.py`
from workout.models.user_model import Users

@pytest.fixture
def app():
    # Set up the Flask test application
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        Users.init_test_data()  # If you have a method to initialize test data

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# Health check
def test_healthcheck(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

# User creation
def test_create_user(client):
    response = client.post("/api/create-user", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 201
    assert response.json["status"] == "user added"
    assert response.json["username"] == "testuser"

# User deletion
def test_delete_user(client):
    client.post("/api/create-user", json={"username": "testuser", "password": "testpass"})
    response = client.delete("/api/delete-user", json={"username": "testuser"})
    assert response.status_code == 200
    assert response.json["status"] == "user deleted"
    assert response.json["username"] == "testuser"

# User login
def test_login_success(client):
    client.post("/api/create-user", json={"username": "testuser", "password": "testpass"})
    response = client.post("/api/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "logged in successfully" in response.json["message"]

def test_login_failure(client):
    response = client.post("/api/login", json={"username": "wronguser", "password": "wrongpass"})
    assert response.status_code == 401
    assert "Invalid username or password" in response.json["error"]

# User logout
def test_logout_success(client):
    client.post("/api/create-user", json={"username": "testuser", "password": "testpass"})
    client.post("/api/login", json={"username": "testuser", "password": "testpass"})
    response = client.post("/api/logout", json={"username": "testuser"})
    assert response.status_code == 200
    assert "logged out successfully" in response.json["message"]

def test_logout_failure(client):
    response = client.post("/api/logout", json={"username": "nonexistentuser"})
    assert response.status_code == 400
    assert "Invalid request payload" in response.json["error"]
