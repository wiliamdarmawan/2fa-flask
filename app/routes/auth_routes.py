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
