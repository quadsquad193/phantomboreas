from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import redis



app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
db.create_all()

redis_client = redis.StrictRedis(**app.config['REDIS_CONN'])

import routes
