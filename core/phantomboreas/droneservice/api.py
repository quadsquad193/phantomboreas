from flask import request, make_response
from flask.views import MethodView
from phantomboreas.db.models import DroneAuth

from phantomboreas.droneservice import process, db_session


class DroneImagesAPI(MethodView):
	def post(self):
		key = request.cookies.get("key")

		if DroneAuth.verify_auth_token(key) != None:
			process.process(request)

			# Return HTTP 204 No Content
			return '', 204
		else:
			return '', 401


class AuthenticateDroneAPI(MethodView):
	def post(self):
		key = request.headers.get("authorization")
		print(key)
		session = db_session()

		drone_auth = session.query(DroneAuth).filter_by(key=key).first()

		if drone_auth != None:
			session_token = drone_auth.generate_auth_token()

			response = make_response('')  
			response.set_cookie('key',value=session_token)

			return response, 204

		return '', 401
