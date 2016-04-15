import json
import time
import datetime

from sqlalchemy import desc

from phantomboreas.webservice import db_session
from phantomboreas.db.models import CitationLog, CaptureLog, PlateLog, CandidateLog



def api_get_interval(timedelta=datetime.timedelta(days=2), since=(datetime.datetime.now() + datetime.timedelta(days=1))):
    session = db_session()

    end_dt = since - timedelta

    q = session.query(CitationLog).\
        join(CitationLog.plate).\
        join(PlateLog.capture).\
        filter(CaptureLog.timestamp.between(end_dt, since))

    citations = q.all()

    citations_repr = [{
        'citation_id':  c.id,
        'status':       {
            'verified':     c.verified,
            'dismissed':    c.dismissed,
            'hidden':       c.hidden,
        },
        'plate':        plate_log_dump(c.plate),
        'evidence':     [plate_log_dump(e) for e in c.evidence],
    } for c in citations]

    return json.dumps({'citations': citations_repr}), 200

def plate_log_dump(plate_log):
    capture_log     = plate_log.capture
    candidate_logs  = plate_log.candidates

    return {
        'candidates':   [{
            'license_plate': c.license_plate,
            'confidence':    c.confidence,
        } for c in candidate_logs],
        'timestamp':    int(time.mktime(capture_log.timestamp.timetuple())),
        'capture_url':  capture_log.filename,
    }
