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
    		capture_list.append({'filename': capture.filename, 'image': b64encode(capture.image)})

        return render_template('index.html', capture_list=capture_list), 200
