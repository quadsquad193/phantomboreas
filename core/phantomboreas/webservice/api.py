from flask import request, send_from_directory
from flask.views import MethodView

from flask import jsonify

from phantomboreas.webservice import app

from phantomboreas.db.models import Base, DroneAuth
from phantomboreas.webservice import db_session

class CaptureAPI(MethodView):
    def get(self, filename):
        return send_from_directory(app.config['IMAGE_STORE_PATH'], filename)


class DroneAuthAPI(MethodView):
	def post(self):
		session = db_session()

		drone_auth = DroneAuth()

		session.add(drone_auth)
		session.commit()

		return jsonify(key=drone_auth.key), 200


