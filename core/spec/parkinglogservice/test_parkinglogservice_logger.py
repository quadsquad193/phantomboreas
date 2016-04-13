import pytest

import tempfile

import sqlalchemy
import datetime
import os

from phantomboreas.parkinglogservice.db import DB
from phantomboreas.parkinglogservice.logger import Logger
from phantomboreas.db.models import Base, CaptureLog, PlateLog, CandidateLog



db_conf = {
    'db_url':   'sqlite://'
}

image = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.jpg'))
TEST_IMAGE_STREAM = image.read()
image.close()

payload = {
    'filename':         'test.jpg',
    'latitude':         38.537002,
    'longitude':        -121.754725,
    'timestamp':        1457395109,
    'image':            TEST_IMAGE_STREAM,
    'process_hash':     'abc123',
    'openalpr_results': [
        {
            "plate": "S11FRE",
            "confidence": 77.130661,
            "matches_template": 0,
            "region": "",
            "region_confidence": 0,
            "coordinates": [
                {"x": 218, "y": 342},
                {"x": 407, "y": 325},
                {"x": 407, "y": 413},
                {"x": 218, "y": 431}
            ],
            "candidates": [
                {"plate": "S11FRE", "confidence": 77.130661, "matches_template": 0},
                {"plate": "S11ERE", "confidence": 75.496307, "matches_template": 0},
                {"plate": "S11RE", "confidence": 75.440361, "matches_template": 0},
                {"plate": "S11CRE", "confidence": 75.340179, "matches_template": 0},
                {"plate": "S11FHE", "confidence": 75.240974, "matches_template": 0}
            ]
        },
        {
            "plate": "EJLESSIE",
            "epoch_time": 1402158050,
            "confidence": 78.167984,
            "matches_template": 0,
            "region": "",
            "region_confidence": 0,
            "processing_time_ms": 51.650604,
            "coordinates": [
                {"x": 226, "y": 369},
                {"x": 348, "y": 348},
                {"x": 355, "y": 406},
                {"x": 231, "y": 429}
            ],
            "candidates": [
                {"plate": "EJLESSIE", "confidence": 78.167984, "matches_template": 0},
                {"plate": "VI5A", "confidence": 58.167984, "matches_template": 0},
                {"plate": "EDLESSIE", "confidence": 77.61319, "matches_template": 0}
            ]
        }
    ]
}



class TestParkingLogServiceLogger:
    # Unconfigured loggers should raise an exception when assert_config() is
    # called
    def test_unconfigured_logger(self):
        logger = Logger(DB())

        with pytest.raises(RuntimeError):
            logger.assert_config()

    # Logger should be able to utilize the SQLAlchemy ORM to persist and
    # retrieve results in a database
    def test_logger_process(self, tmpdir):
        db = DB()
        logger = Logger(db)

        db.config(db_conf)
        logger.config({
            'image_store_path': str(tmpdir.realpath())
        })

        session = db.session()

        logger.process(payload)

        capture_log = session.query(CaptureLog).first()
        assert capture_log.filename         == 'test.jpg'
        assert float(capture_log.latitude)  == 38.5370020
        assert float(capture_log.longitude) == -121.7547250
        assert capture_log.timestamp        == datetime.datetime.fromtimestamp(1457395109)

        assert session.query(PlateLog).count() == 2
        plate_log = session.query(PlateLog).first()
        assert plate_log.upper_left_x   == 218
        assert plate_log.upper_left_y   == 342
        assert plate_log.upper_right_x  == 407
        assert plate_log.upper_right_y  == 325
        assert plate_log.lower_right_x  == 407
        assert plate_log.lower_right_y  == 413
        assert plate_log.lower_left_x   == 218
        assert plate_log.lower_left_y   == 431

        assert session.query(CandidateLog).count() == 8
        candidate_log = session.query(CandidateLog).first()
        candidates = session.query(CandidateLog.license_plate).filter(CandidateLog.license_plate.like('%ESS%')).all()
        assert ('EJLESSIE',) in candidates
        assert ('EDLESSIE',) in candidates

        assert plate_log in capture_log.plates
        assert plate_log.capture == capture_log

        assert candidate_log in plate_log.candidates
        assert candidate_log.plate == plate_log

        assert tmpdir.join('test.jpg').read() == TEST_IMAGE_STREAM
