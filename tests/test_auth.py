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

