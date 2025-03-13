from flask import Blueprint, request, jsonify
from app import db, bcrypt, errors
from app.models import User
from app.services.email_service import send_email
from app.services.user_service import generate_username
from app.services.otp_service import generate_otp, store_otp, verify_otp
from app.utils.params_helper import validate_json_api_params
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import re
import random

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    params = validate_json_api_params(request.json)

    email = params.get("email")
    password = params.get("password")

    if not email or not password:
        raise errors.MissingParamsError("Email and password required")
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise errors.InvalidParamsError("Provided email is not an email address")

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    username = generate_username(email)

    try:
        user = User(email=email, username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback to avoid partial commits
        raise e

    return jsonify(
        {
            "data": {
                "id": user.id,
                "attributes": {
                    "username": user.username
                }
            }
        }
    ), 201
