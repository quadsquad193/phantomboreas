from flask import request, jsonify
from sqlalchemy import desc

import time
import datetime

from phantomboreas.webservice import db_session
from phantomboreas.db.models import CitationLog, CaptureLog, PlateLog, CandidateLog



def api_get_citation(capture_id):
    session = db_session()

    citation_log = session.query(CitationLog).get(capture_id)

    if citation_log is None:
        return jsonify({}), 404

    citation = citation_log_dump(citation_log)

    return jsonify({'success': True, 'citation': citation_log_dump(citation_log)}), 200

def api_put_citation(capture_id):
    session = db_session()

    citation_log = session.query(CitationLog).get(capture_id)

    if citation_log is None:
        return jsonify({'success': False, 'message': 'Citation not found.'}), 404

    delegate(session, citation_log, request.form.get('delegate_to', None, type=int))
    verify(session, citation_log, bool_option(request.form.get('verify', None)))
    dismiss(session, citation_log, bool_option(request.form.get('dismiss', None)))

    session.add(citation_log)
    session.commit()

    return jsonify({'success': True, 'citation': citation_log_dump(citation_log)}), 200

def delegate(session, citation_log, new_delegate_id=None):
    if new_delegate_id is None: return
    if new_delegate_id == citation_log.id: return

    # Remove delegate
    if new_delegate_id == 0:
        citation_log.delegate = None
        return

    new_delegate = session.query(CitationLog).get(new_delegate_id)

    # No such citation exists
    if new_delegate is None: return

    # Remove old delegate
    citation_log.delegate = None

    # Traverse self-referential relation "tree" until we reach the root delegate
    while(new_delegate.delegate): new_delegate = new_delegate.delegate

    # Set new delegate
    citation_log.delegate = new_delegate

def verify(session, citation_log, verify=None):
    if verify is None: return

    citation_log.verified = verify
    if verify: citation_log.dismissed = False

def dismiss(session, citation_log, dismiss=None):
    if dismiss is None: return

    citation_log.dismissed = dismiss
    if dismiss: citation_log.verified = False

def api_get_citations_list(timedelta=datetime.timedelta(days=2), since=(datetime.datetime.now() + datetime.timedelta(days=1))):
    session = db_session()

    filter_verified     = bool_option(request.args.get('verified', None))
    filter_dismissed    = bool_option(request.args.get('dismissed', None))
    filter_delegator    = bool_option(request.args.get('delegator', None))

    end_dt = since - timedelta

    q = session.query(CitationLog).\
        join(CitationLog.plate).\
        join(PlateLog.capture).\
        filter(CaptureLog.timestamp.between(end_dt, since))

    if filter_verified is not None:
        q = q.filter(CitationLog.verified.is_(filter_verified))

    if filter_dismissed is not None:
        q = q.filter(CitationLog.dismissed.is_(filter_dismissed))

    if filter_delegator is not None:
        if filter_delegator:
            q = q.filter(CitationLog.delegate_id.isnot(None))
        else:
            q = q.filter(CitationLog.delegate_id.is_(None))

    citations = q.all()

    citations_repr = [citation_log_dump(c) for c in citations]

    return jsonify({'citations': citations_repr}), 200

def api_search_citation():
    session = db_session()

    start_datetime      = datetime_option(request.args.get('start_datetime', None))
    end_datetime        = datetime_option(request.args.get('end_datetime', None))
    license_plate       = upperstring_option(request.args.get('license_plate', None))

    if not len(filter(lambda x: x is not None, [start_datetime, end_datetime, license_plate])):
        return jsonify({'success': False, 'message': 'No search parameters found.'}), 400

    if ((start_datetime is None and end_datetime is not None) or (start_datetime is not None and end_datetime is None)):
        return jsonify({'success': False, 'message': 'There must be a pair of dates & times or none.'}), 400

    q = session.query(CitationLog).\
        join(CitationLog.plate).\
        join(PlateLog.capture)

    if start_datetime is not None and end_datetime is not None:
        q = q.order_by(CaptureLog.timestamp.desc()).\
            filter(CaptureLog.timestamp.between(start_datetime, end_datetime))

    if license_plate is not None:
        q = q.join(PlateLog.candidates).\
            filter(CandidateLog.license_plate == license_plate)

    citations = q.all()

    citations_repr = [citation_log_dump(c) for c in citations]

    return jsonify({'citations': citations_repr}), 200

def bool_option(val):
    return True if val == 'true' else False if val == 'false' else None

def datetime_option(val):
    if val is None or not val: return None
    dt = None
    try:
        dt = datetime.datetime.strptime(val, "%Y-%m-%dT%H:%M")
    except ValueError:
        dt = None
    return dt

def upperstring_option(val):
    if val is None or not val: return None
    return str(val).strip().upper()

def citation_log_dump(citation_log):
    return {
        'citation_id':  citation_log.id,
        'status':       {
            'verified':     citation_log.verified,
            'dismissed':    citation_log.dismissed,
            'delegate_to':   citation_log.delegate_id,
            'delegations':  [d.id for d in citation_log.delegations],
        },
        'plate':        plate_log_dump(citation_log.plate),
        'evidence':     [plate_log_dump(e) for e in citation_log.evidence],
    }

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
        'coordinates': {
            'longitude':    float(capture_log.longitude),
            'latitude':     float(capture_log.latitude),
        }
    }
