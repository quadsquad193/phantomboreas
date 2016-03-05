from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from parkinglogservice.db.models import Base, LicensePlateLog
from parkinglogservice import utils



class Logger(object):
    def __init__(self):
        self.configured = False
        self.db_engine  = None

        self.db_session = sessionmaker()

    def config(self, db_conf):
        self.db_engine = create_engine(db_conf['sqlite_url'])

        self.db_session.configure(bind=self.db_engine)
        Base.metadata.create_all(self.db_engine)

        self.configured = True

    def assert_config(self):
        if not self.configured: raise RuntimeError("Logger not yet configured with config() method.")

    def process(self, payload):
        # TODO: do stuff with the OpenALPR results

        utils.debug_print_results(payload['openalpr_results'])

        # create new DB session to handle any transactions
        session = self.db_session()

        log = LicensePlateLog(id='test')

        session.add(log)
        session.commit()
