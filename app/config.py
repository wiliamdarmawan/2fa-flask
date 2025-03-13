class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://root:root@db/2fa_db"
    SMTP_HOST = "smtp-relay.brevo.com"
    SMTP_PORT = 587
    SMTP_USERNAME = "87d572001@smtp-brevo.com"
    SMTP_PASSWORD = "8hCr7jBEysDqRSvW"
    CELERY_BROKER_URL= "redis://redis:6379/0"
    CELERY_RESULT_BACKEND= "redis://redis:6379/0"
