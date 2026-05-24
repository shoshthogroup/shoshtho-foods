import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'shoshtho-secret-2026'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///shoshtho.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CASH_ON_DELIVERY = True
    BKASH_ENABLED = True
