from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

from phantomboreas.db.models import Base, CaptureLog, PlateLog, CandidateLog



class Logger(object):
    def __init__(self):
        self.configured = False
        self.db_engine  = None

        self.db_session = sessionmaker()

    def config(self, db_conf):
        self.db_engine = create_engine(db_conf['db_url'])

        self.db_session.configure(bind=self.db_engine)
        Base.metadata.create_all(self.db_engine)

        self.configured = True

    def assert_config(self):
        if not self.configured: raise RuntimeError("Logger not yet configured with config() method.")

    def process(self, payload):
        # create new DB session to handle any transactions
        session = self.db_session()

        capture_log = CaptureLog(
            image=payload['image'],
            filename=payload['filename'],
            latitude=payload['latitude'],
            longitude=payload['longitude'],
            timestamp=datetime.datetime.fromtimestamp(payload['timestamp'])
        )

        # ... each CaptureLog has possibly many PlateLogs
        for plate_result in payload['openalpr_results']:
            # coordinates is an array of Cartesian points, in clockwise-order
            # starting from the top-left "corner" of the bounding polygon
            coordinates = plate_result['coordinates']

            plate_log = PlateLog(
                upper_left_x    = coordinates[0]['x'],
                upper_left_y    = coordinates[0]['y'],
                upper_right_x   = coordinates[1]['x'],
                upper_right_y   = coordinates[1]['y'],
                lower_right_x   = coordinates[2]['x'],
                lower_right_y   = coordinates[2]['y'],
                lower_left_x    = coordinates[3]['x'],
                lower_left_y    = coordinates[3]['y']
            )

            # ... each PlateLog has possibly many CandidateLogs
            for candidate_result in plate_result['candidates']:
                candidate = CandidateLog(
                    license_plate=candidate_result['plate'],
                    confidence=candidate_result['confidence']
                )

                plate_log.candidates.append(candidate)

            capture_log.plates.append(plate_log)

        session.add(capture_log)
        session.commit()
