import random
from datetime import timedelta
from app import redis_client

def generate_otp():
    return str(random.randint(100000, 999999))

def store_otp(email, otp):
    redis_client.setex(email, timedelta(minutes=30), otp)

def verify_otp(email, otp):
    stored_otp = redis_client.get(email)
    return stored_otp == otp
