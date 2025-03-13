from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import redis
from app.config import Config
from app.errors import register_error_handlers
from celery import Celery

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
redis_client = redis.StrictRedis(host="redis", port=6379, decode_responses=True)
celery = Celery(__name__, include=["app.services.email_service"])

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    register_error_handlers(app)

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"]
    )

    return app
