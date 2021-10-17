from flask import Flask
from flask_cors import CORS
import flask_restful as restful
from flask_restful import Resource, Api,reqparse

from flask_sqlalchemy import SQLAlchemy
# from flask_mongoengine import MongoEngine
from sqliteconfig import config

app = Flask(__name__)

CORS(app)

app.config.from_object(config['development'])
app.app_context().push()
db = SQLAlchemy()
db.init_app(app)
db.app = app
