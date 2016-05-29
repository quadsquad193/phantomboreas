import config
import sqlalchemy

engine = sqlalchemy.create_engine(config.SQLALCHEMY_DATABASE_DEFINITION) # connect to server
engine.execute("DROP DATABASE IF EXISTS " + config.SQLALCHEMY_DATABASE_NAME) #create db
