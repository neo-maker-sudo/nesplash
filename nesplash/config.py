import os
from redis import Redis

class BaseConfig():
    # SERVER_NAME = "www.nesplash.tw"
    # PREFERRED_URL_SCHEME = "https"
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WHOOSHEE_MIN_STRING_LEN = 1
    TF_CPP_MIN_LOG_LEVEL = 3
    MAIN_PER_PAGE = 10

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = '6379'

    # authy
    AUTHY_APP_NAME = os.getenv("AUTHY_APP_NAME")
    AUTHY_APP_ID = os.getenv("AUTHY_APP_ID")
    AUTHY_PRODUCTION_API_KEY = os.getenv("AUTHY_PRODUCTION_API_KEY")

    # session
    SESSION_TYPE = "redis"
    SESSION_REDIS = Redis(  
        host='127.0.0.1',  
        port=6379)
    SESSION_USE_SIGNER = True
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 3600

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://neo:{os.getenv('NEO_MYSQL')}@localhost:3306/nesplash?charset=utf8mb4"
    ADMIN_EMAIL = os.getenv("ADMIN_ACCOUNT")


class TestingConfig(BaseConfig):
    TESTING = True
    ADMIN_EMAIL = os.getenv("ADMIN_ACCOUNT")
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    
config = {
    "development": DevelopmentConfig,
    "TESTING": TestingConfig
}
