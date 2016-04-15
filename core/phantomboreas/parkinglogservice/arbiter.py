from sqlalchemy import desc

from phantomboreas.db.models import Base, CaptureLog, PlateLog, CandidateLog, CitationLog



class Arbiter(object):
    def __init__(self, db):
        self.configured = False

        self.db = db

    def config(self, rules_conf):
        self.limit = rules_conf['limit']
        self.grace = rules_conf['grace']

        self.configured = True

    def assert_config(self):
        if not self.configured: raise RuntimeError("Arbiter not yet configured with config() method.")

        self.db.assert_config()

    def process(self, capture_log):
        # Given a captured image at some definite time...

        session = self.db.session()

        # Relevant interval times for a particular capture
        capture_dt = capture_log.timestamp
        upper_dt = capture_dt - self.limit
        lower_dt = upper_dt - self.grace

        # For each plate recognized in a capture
        for plate_log in capture_log.plates:
            # Create a Python-level list of candidate (possible) license plates
            candidate_plates = [c.license_plate for c in plate_log.candidates]

            # Query the DB for other plate logs (an abstract representation of
            # a collection of many candidate plate readings) whose candidates
            # are in the aforementioned list of candidates.
            q = session.query(PlateLog).\
                join(PlateLog.candidates).\
                join(PlateLog.capture).\
                filter(CaptureLog.timestamp.between(lower_dt, upper_dt)).\
                filter(CandidateLog.license_plate.in_(candidate_plates)).\
                order_by(desc(CaptureLog.timestamp))

            # The result set may contain multiple entries of the same PlateLog
            # (e.g; when multiple candidate matches are present between two
            # PlateLo). We only need a set of unique PlateLogs.
            q = q.distinct(PlateLog.id)

            pairing_plate_logs = q.all()
            if (len(pairing_plate_logs)):
                # Create a citation
                citation = CitationLog(plate=plate_log)
                for paired_plate_log in pairing_plate_logs:
                    citation.evidence.append(paired_plate_log)
                session.add(citation)

        session.commit()
