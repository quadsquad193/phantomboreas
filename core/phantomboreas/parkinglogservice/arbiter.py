import datetime
import os

from phantomboreas.db.models import Base, CaptureLog, PlateLog, CandidateLog



class Arbiter(object):
    def __init__(self, db):
        self.configured = False

        self.db = db

    def config(self):
        self.configured = True

    def assert_config(self):
        if not self.configured: raise RuntimeError("Logger not yet configured with config() method.")

        self.db.assert_config()

    def process(self, capture_log):
        pass
