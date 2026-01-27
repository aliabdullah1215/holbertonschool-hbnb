import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key"
    JWT_SECRET_KEY = SECRET_KEY
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True

