import os


class BaseConfig():
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIN_PER_PAGE = 10

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://neo:{os.getenv('NEO_MYSQL')}@localhost:3306/nesplash?charset=utf8mb4"
    ADMIN_EMAIL = "zhangneo1031@gmail.com"

config = {
    "development": DevelopmentConfig
}
