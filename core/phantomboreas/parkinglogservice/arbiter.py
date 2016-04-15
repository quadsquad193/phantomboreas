import datetime
from sqlalchemy import desc

from phantomboreas.db.models import Base, CaptureLog, PlateLog, CandidateLog, CitationLog



class Arbiter(object):
    def __init__(self, db):
        self.configured = False

        self.db = db

    def config(self, rules_conf):
        self.limit          = rules_conf['timedelta_limit']
        self.hot            = rules_conf['timedelta_hot']
        self.start          = rules_conf['time_start']
        self.end            = rules_conf['time_end']
        self.days           = [{
            'sunday':       0,
            'monday':       1,
            'tuesday':      2,
            'wednesday':    3,
            'thursday':     4,
            'friday':       5,
            'saturday':     6,
        }.get(day_name, None) for (day_name, enforce) in rules_conf['days_enforced'].iteritems() if enforce]
        self.gps_proximity  = rules_conf['gps_proximity']

        self.configured = True

    def assert_config(self):
        if not self.configured: raise RuntimeError("Arbiter not yet configured with config() method.")

        self.db.assert_config()

    def process(self, capture_log):
        # Given a captured image at some definite time...

        session = self.db.session()

        # Datetime and Time of capture
        capture_dt          = capture_log.timestamp
        capture_d           = capture_dt.date()

        # Don't process if capture is not within daily time limits or on day of
        # weekly enforcement
        if  (capture_dt < (datetime.datetime.combine(capture_d, self.start) + self.limit)) or \
            (capture_dt > datetime.datetime.combine(capture_d, self.end)) or \
            (capture_d.weekday() not in self.days):
            return

        # Relevant time and spatial ranges particular capture
        upper_dt            = capture_dt - self.limit
        lower_dt            = upper_dt - self.hot
        capture_latitude    = float(capture_log.latitude)
        capture_longitude   = float(capture_log.longitude)
        latitude_lower      = capture_latitude - self.gps_proximity
        latitude_upper      = capture_latitude + self.gps_proximity
        longitude_lower     = capture_longitude - self.gps_proximity
        longitude_upper     = capture_longitude + self.gps_proximity

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
                order_by(desc(CaptureLog.timestamp))

            # Filter on offending time interval
            q = q.filter(CaptureLog.timestamp.between(lower_dt, upper_dt))

            # Filter on candidate plate intersection via string matching
            q = q.filter(CandidateLog.license_plate.in_(candidate_plates))

            # Filter geospatially by GPS range
            q = q.\
                filter(CaptureLog.latitude.between(latitude_lower, latitude_upper)).\
                filter(CaptureLog.longitude.between(longitude_lower, longitude_upper))

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
