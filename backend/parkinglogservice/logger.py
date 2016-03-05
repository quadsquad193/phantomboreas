from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from parkinglogservice.db.models import Base, CandidateLog, CaptureLog
from parkinglogservice import utils

import datetime

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

        capture_log = CaptureLog(
            filename=payload['filename'], latitude=payload['latitude'], longitude=payload['longitude'],
            timestamp=datetime.date.fromtimestamp(payload['timestamp']), image=payload['image']
        )

        # Build new candidates
        for result in payload['openalpr_results']:
            for candidate in result['candidates']:
                capture_log.candidates.append(
                    CandidateLog(license_plate=candidate['plate'], confidence=candidate['confidence'])
                )

        session.add(capture_log)
        session.commit()
