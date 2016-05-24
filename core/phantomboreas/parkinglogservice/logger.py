import datetime
from werkzeug.utils import secure_filename
import os

from phantomboreas.db.models import Base, CaptureLog, PlateLog, CandidateLog



class Logger(object):
    def __init__(self, db):
        self.configured = False

        self.db = db

    def config(self, assets_conf):
        self.image_store_path = assets_conf['image_store_path']

        self.configured = True

    def assert_config(self):
        if not self.configured: raise RuntimeError("Logger not yet configured with config() method.")

        self.db.assert_config()

    def save_on_disk(self, filename, image):
        if ('.' not in filename) or (filename.rsplit('.', 1)[1] not in ['jpg', 'jpeg', 'png']):
            return None

        filepath = os.path.join(self.image_store_path, secure_filename(filename))

        fd = open(filepath, 'w')
        fd.write(image)
        fd.close()

        return filepath

    def process(self, payload):
        # save image on disk
        filepath = self.save_on_disk(payload['filename'], payload['image'])

        # create new DB session to handle any transactions
        session = self.db.session()

        capture_log = CaptureLog(
            filepath=filepath,
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

        return capture_log
