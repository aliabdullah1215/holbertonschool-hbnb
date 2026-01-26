#!/usr/bin/python3
"""Application configuration"""

class Config:
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    "default": Config,
    "development": DevelopmentConfig
}
