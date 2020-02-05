from flask import Flask, Blueprint
from config import Config
from flask_mongoengine import MongoEngine
from flask_restplus import Api
from flask_jwt_simple import JWTManager

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint,
          title='Time Tracking API',
          version='v0.1',
          description='RESTful API built for the Time Tracking APP in order to perform load operations in warehouse.',
          default='Available Methods/Endpoints',
          default_label=None)
app.register_blueprint(blueprint)
app.config.from_object(Config)

jwt = JWTManager(app)

db = MongoEngine()
db.init_app(app)
#api.init_app(app)

from application import routes

