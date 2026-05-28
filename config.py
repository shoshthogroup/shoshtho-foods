import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ── Strong Secret Key ──
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        os.urandom(32).hex()

    # ── Database ──
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get('DATABASE_URL') or \
        'sqlite:///shoshtho.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Session Security ──
    SESSION_COOKIE_SECURE = False  # True in production
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

    # ── File Upload ──
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max

    # ── Payment ──
    BKASH_ENABLED = True
    CASH_ON_DELIVERY = True

class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True