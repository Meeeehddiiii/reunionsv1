# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mehdi:12345@db:3306/reunions'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '12345'
