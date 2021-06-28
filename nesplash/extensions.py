from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_mail import Mail
from flask_oauthlib.client import OAuth

db = SQLAlchemy()
ma = Marshmallow()
cors = CORS()
mail = Mail()
oauth = OAuth()
