import pytest
from flask import Flask
from app import app  # Import your Flask app instance from app.py


@pytest.fixture
def client():
    """Fixture to provide a test client for the Flask app."""
    with app.test_client() as client:
        yield client


def test_create_account_success(client):
    """Test successful account creation."""
    response = client.post('/api/create-account', json={
        'username': 'testuser',
        'password': 'securepassword'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Account created successfully'


def test_create_account_duplicate(client):
    """Test creating an account with a duplicate username."""
    client.post('/api/create-account', json={
        'username': 'testuser',
        'password': 'securepassword'
    })
    response = client.post('/api/create-account', json={
        'username': 'testuser',
        'password': 'securepassword2'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Username already exists'


def test_login_success(client):
    """Test successful login."""
    client.post('/api/create-account', json={
        'username': 'testuser',
        'password': 'securepassword'
    })
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'securepassword'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Login successful'


def test_login_invalid_password(client):
    """Test login with an incorrect password."""
    client.post('/api/create-account', json={
        'username': 'testuser',
        'password': 'securepassword'
    })
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid username or password'


def test_update_password_success(client):
    """Test successful password update."""
    client.post('/api/create-account', json={
        'username': 'testuser',
        'password': 'securepassword'
    })
    response = client.post('/api/update-password', json={
        'username': 'testuser',
        'old_password': 'securepassword',
        'new_password': 'newsecurepassword'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Password updated successfully'

    # Test login with the new password
    login_response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'newsecurepassword'
    })
    assert login_response.status_code == 200
    assert login_response.json['message'] == 'Login successful'


def test_update_password_invalid_old_password(client):
    """Test password update with incorrect old password."""
    client.post('/api/create-account', json={
        'username': 'testuser',
        'password': 'securepassword'
    })
    response = client.post('/api/update-password', json={
        'username': 'testuser',
        'old_password': 'wrongpassword',
        'new_password': 'newsecurepassword'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Old password is incorrect'
