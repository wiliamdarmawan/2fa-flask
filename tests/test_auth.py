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

