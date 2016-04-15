from flask import request, send_from_directory
from flask.views import MethodView

from flask import jsonify
from flask import request

from phantomboreas.webservice import app, bcrypt

from flask.ext.security import login_required

from phantomboreas.db.models import Base, DroneAuth, User
from phantomboreas.webservice import db_session

class CaptureAPI(MethodView):
	@login_required
	def get(self, filename):
		return send_from_directory(app.config['IMAGE_STORE_PATH'], filename)


class DroneAuthAPI(MethodView):
	@login_required
	def post(self):
		session = db_session()

		drone_auth = DroneAuth()

		session.add(drone_auth)
		session.commit()

		return jsonify(key=drone_auth.key), 200


class TestUsersAPI(MethodView):
	def get(self):
		userID = request.args.get('userID')
		plaintext = request.args.get('plaintext')

		session = db_session()

		user = session.query(User).filter_by(id=userID).first()

		if bcrypt.check_password_hash(user.password, plaintext):
			return jsonify({}), 200

		return jsonify({}), 403


	def post(self):
		session = db_session()

		user = User(username='mhmachado', password=bcrypt.generate_password_hash('password'), is_admin=True)

		session.add(user)
		session.commit()

		return jsonify({'id': user.id}), 200

