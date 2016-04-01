from flask import request
from flask.views import MethodView
from flask import render_template
# import sqlalchemy as sa
# from sqlalchemy import orm
# from sqlalchemy import create_engine
from base64 import b64encode

from phantomboreas.db.models import Base, CaptureLog, PlateLog, CandidateLog
from phantomboreas.webservice import db_session
import process



class IndexView(MethodView):
    def get(self):
    	session = db_session()

    	_capture_list = session.query(CaptureLog).all()
    	capture_list = []

    	for capture in _capture_list:
    		#Get necessary capture info and put it in json format
    		c = {'filename': capture.filename, 'image': b64encode(capture.image), 'plates': []}

    		#Add necessary information about plates and candidates
    		for plate in capture.plates:
    			p = {'id': plate.id, 'candidates': []}

    			for candidate in plate.candidates:
    				p['candidates'].append({'license_plate': candidate.license_plate, 'confidence': candidate.confidence})

    			c['plates'].append(p)

    		capture_list.append(c)

        return render_template('index.html', capture_list=capture_list), 200

