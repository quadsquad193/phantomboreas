from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis


app = Flask(__name__)
app.config.from_object('config')

db_session = sessionmaker()
db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db_session.configure(bind=db_engine)

redis_client = redis.StrictRedis(
    host=app.config['REDIS_CONN']['host'],
    port=app.config['REDIS_CONN']['port'],
    db=app.config['REDIS_CONN']['db_index']
)

import routes
