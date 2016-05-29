from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from phantomboreas.db.models import Base



class DB(object):
    def __init__(self):
        self.configured = False
        self.db_engine  = None

        self.db_session = sessionmaker()

    def config(self, db_conf):
        self.db_engine = create_engine(db_conf['db_url'])

        self.db_session.configure(bind=self.db_engine)
        self.db_session = scoped_session(self.db_session)
        Base.metadata.create_all(self.db_engine)

        self.configured = True

    def assert_config(self):
        if not self.configured: raise RuntimeError("DB not yet configured with config() method.")

    def session(self):
        self.assert_config()

        return self.db_session()
