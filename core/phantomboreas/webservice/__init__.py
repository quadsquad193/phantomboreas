from flask import Flask
from flask.ext.login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis

from phantomboreas.db.models import Base, User

from flask.ext.bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_object('config')

bcrypt = Bcrypt(app)

db_session = sessionmaker()
db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db_session.configure(bind=db_engine)
Base.metadata.create_all(db_engine)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view =  "signin"

@login_manager.user_loader
def load_user(userid):
	session = db_session()
	return session.query(User).filter(User.id == userid).first()

redis_client = redis.StrictRedis(
    host=app.config['REDIS_CONN']['host'],
    port=app.config['REDIS_CONN']['port'],
    db=app.config['REDIS_CONN']['db_index']
)

import routes
