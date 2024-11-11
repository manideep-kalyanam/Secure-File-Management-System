# config.py
import os

class Config:
    # SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SECRET_KEY = os.urandom(24)
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'fcs_project'
