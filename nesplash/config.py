import os

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

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://neo:{os.getenv('NEO_MYSQL')}@localhost:3306/nesplash?charset=utf8mb4"
    ADMIN_EMAIL = os.getenv("ADMIN_ACCOUNT")


config = {
    "development": DevelopmentConfig
}
