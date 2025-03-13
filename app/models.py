from app import db
from sqlalchemy.orm import validates
import re
from app import errors

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), index=True, unique=True, nullable=False)
    username = db.Column(db.String(30), index=True, unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    @validates("email") 
    def validate_email(self, key, email):
        if not email:
            raise errors.InvalidParamsError("No email provided")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise errors.InvalidParamsError("Provided email is not an email address") 
        elif User.query.filter(User.email == email).first():
            raise errors.InvalidParamsError("Email already exists")
        elif len(email) > 320:
            raise errors.InvalidParamsError("Email must be less than or equal to 320 characters")
        return email

    @validates("username") 
    def validate_username(self, key, username):
        if not username:
            raise errors.InvalidParamsError("No username provided")
        elif User.query.filter(User.username == username).first():
            raise errors.InvalidParamsError("Username is already in use, please retry your request")
        elif len(username) < 3 or len(username) > 30:
            raise errors.InvalidParamsError("Username must be between 3 and 30 characters") 
        return username
