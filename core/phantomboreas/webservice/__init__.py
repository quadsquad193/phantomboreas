from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis
import config
from db.models import Base

app = Flask(__name__)
app.config.from_object('config')

db_conf = {
    'sqlite_url':   config.SQLALCHEMY_DATABASE_URI
 }


db_session = sessionmaker()
db_engine = create_engine(db_conf['sqlite_url'])
db_session.configure(bind=db_engine)
Base.metadata.create_all(db_engine)


redis_client = redis.StrictRedis(
    host=app.config['REDIS_CONN']['host'],
    port=app.config['REDIS_CONN']['port'],
    db=app.config['REDIS_CONN']['db_index']
)

import routes
