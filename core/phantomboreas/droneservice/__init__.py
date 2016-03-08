from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import redis



app = Flask(__name__)
app.config.from_object('config')

redis_client = redis.StrictRedis(
    host=app.config['REDIS_CONN']['host'],
    port=app.config['REDIS_CONN']['port'],
    db=app.config['REDIS_CONN']['db_index']
)

import routes
