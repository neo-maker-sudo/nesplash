import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_mail import Mail
from flask_oauthlib.client import OAuth
from keras.applications.vgg16 import VGG16
from flask_whooshee import Whooshee
from flask_caching import Cache


db = SQLAlchemy()
ma = Marshmallow()
cors = CORS()
mail = Mail()
oauth = OAuth()
whooshee = Whooshee()
cache = Cache()
model = VGG16(weights='imagenet', include_top=True)

