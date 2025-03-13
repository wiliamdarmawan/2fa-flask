from flask import Blueprint, request, jsonify
from app import db, bcrypt, errors, limiter
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

@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    params = validate_json_api_params(request.json)

    email = params.get("email")
    password = params.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        raise errors.UnauthorizedError("Invalid credentials")

    otp = generate_otp()
    store_otp(email, otp)
    send_email.delay(email, "Your OTP Code", f"Your OTP is: {otp}")

    return jsonify({"message": "OTP sent to email"}), 200

@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp_route():
    params = validate_json_api_params(request.json)

    email = params.get("email")
    otp = params.get("otp")

    if verify_otp(email, otp):
        access_token = create_access_token(identity=email)
        return jsonify({"access_token": access_token}), 200
    else:
        raise errors.UnauthorizedError("Invalid or expired OTP")

# Protected route
@auth_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()

    if not user:
        raise errors.UnauthorizedError("Invalid JWT Token")
    
    return jsonify({
        "status": "success",
        "message": f"Hey {user.username}, you are welcome"
    }), 200