import pytest
from app import create_app, db, bcrypt
from app.models import User
from unittest.mock import patch
from flask_jwt_extended import decode_token, create_access_token
import os

@pytest.fixture
def app():
    os.environ["FLASK_ENV"] = "testing" 
    os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_without_email(client):
    response = client.post("/register", json={
        "data": {
            "attributes": {
                "email": "",
                "password" : "securepassword"
            }
        }
    })
    assert response.status_code == 400
    assert response.json == {
        "errors": [
            {
                "error": "Email and password required",
                "errorCode": "TFAE2",
                "errorHandling": "Please include the missing parameter."
            }
        ]
    }

    response = client.post("/register", json={
        "data": {
            "attributes": {
                "password" : "securepassword"
            }
        }
    })
    assert response.status_code == 400
    assert response.json == {
        "errors": [
            {
                "error": "Email and password required",
                "errorCode": "TFAE2",
                "errorHandling": "Please include the missing parameter."
            }
        ]
    }

def test_register_without_password(client):
    response = client.post("/register", json={
        "data": {
            "attributes": {
                "email": "test@gmail.com",
                "password" : ""
            }
        }
    })
    assert response.status_code == 400
    assert response.json == {
        "errors": [
            {
                "error": "Email and password required",
                "errorCode": "TFAE2",
                "errorHandling": "Please include the missing parameter."
            }
        ]
    }

    response = client.post("/register", json={
        "data": {
            "attributes": {
                "email": "test@gmail.com"
            }
        }
    })
    assert response.status_code == 400
    assert response.json == {
        "errors": [
            {
                "error": "Email and password required",
                "errorCode": "TFAE2",
                "errorHandling": "Please include the missing parameter."
            }
        ]
    }

def test_register_invalid_email_format(client):
    response = client.post("/register", json={
        "data": {
            "attributes": {
                "email": "testingemail.com",
                "password": "securepassword",
            }
        }
    })

    assert response.status_code == 400
    assert response.json == {
        "errors": [
            {
                "error": "Provided email is not an email address",
                "errorCode": "TFAE1",
                "errorHandling": "Please provide a valid parameter."
            }
        ]
    }

def test_register_existing_email(client, mocker):
    mocker.patch("app.routes.auth_routes.generate_username", return_value="testuser")

    user = User(email="test@example.com", username="testuser", password="hashedpassword")
    db.session.add(user)
    db.session.commit()

    response = client.post("/register", json={
        "data": {
            "attributes": {
                "email": "test@example.com",
                "password": "securepassword"
            }
        }
    })

    assert User.query.count() == 1
    assert response.status_code == 400
    assert response.json == {
        "errors": [
            {
                "error": "Email already exists",
                "errorCode": "TFAE1",
                "errorHandling": "Please provide a valid parameter."
            }
        ]
    }

def test_register_existing_username(client, mocker):
    mocker.patch("app.routes.auth_routes.generate_username", return_value="testuser")

    user = User(email="test@example.com", username="testuser", password="hashedpassword")
    db.session.add(user)
    db.session.commit()

    response = client.post("/register", json={
        "data": {
            "attributes": {
                "email": "testing1@example.com",
                "password": "securepassword"
            }
        }
    })

    assert User.query.count() == 1
    assert response.status_code == 400
    assert response.json == {
        "errors": [
            {
                "error": "Username is already in use, please retry your request",
                "errorCode": "TFAE1",
                "errorHandling": "Please provide a valid parameter."
            }
        ]
    }

def test_register_success(client, mocker):
    mocker.patch("app.routes.auth_routes.generate_username", return_value="testuser")

    response = client.post("/register", json={
        "data": {
            "attributes": {
                "email": "test@example.com",
                "password": "securepassword"
            }
        }
    })

    assert User.query.count() == 1
    assert response.status_code == 201
    assert response.json == {
        "data": {
            "id": User.query.first().id,
            "attributes": {
                "username": "testuser"
            }
        }
    }

def test_login_user_not_found(client):
    response = client.post("/login", json={
        "data": {
            "attributes": {
                "email": "foo",
                "password" : "bar"
            }
        }
    })

    assert response.status_code == 401
    assert response.json == {
        "errors": [
            {
                "error": "Invalid credentials",
                "errorCode": "TFAE3",
                "errorHandling": "Please provide correct credentials"
            }
        ]
    }

def test_login_with_wrong_password(client):
    user = User(email="test@example.com", username="testuser", password=bcrypt.generate_password_hash("randompassword").decode("utf-8"))
    db.session.add(user)
    db.session.commit()

    response = client.post("/login", json={
        "data": {
            "attributes": {
                "email": "test@example.com",
                "password": "securepassword"
            }
        }
    })

    assert response.status_code == 401
    assert response.json == {
        "errors": [
            {
                "error": "Invalid credentials",
                "errorCode": "TFAE3",
                "errorHandling": "Please provide correct credentials"
            }
        ]
    }

def test_login_success(client, mocker):
    mocker.patch("app.routes.auth_routes.generate_otp", return_value="123456")
    mock_store_otp = mocker.patch("app.routes.auth_routes.store_otp")
    mock_send_email = mocker.patch("app.routes.auth_routes.send_email.delay")

    password = "securepassword"
    user = User(email="test@example.com", username="testuser", password=bcrypt.generate_password_hash(password).decode("utf-8"))
    db.session.add(user)
    db.session.commit()

    response = client.post("/login", json={
        "data": {
            "attributes": {
                "email": "test@example.com",
                "password": password
            }
        }
    })

    assert response.status_code == 200
    assert response.json["message"] == "OTP sent to email"
    mock_store_otp.assert_called_once()
    mock_send_email.assert_called_once()

