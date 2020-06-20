from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)

from statistic.statistic_resource import ActionAddResource, ActionListResource

api.add_resource(ActionListResource, '/statistic')
api.add_resource(ActionAddResource, '/statistic/add')

# Migration
from statistic import statistic_model
