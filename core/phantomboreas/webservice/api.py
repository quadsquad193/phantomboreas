from flask import request, send_from_directory, make_response, redirect, url_for
from flask.views import MethodView

from flask import jsonify
from flask import request, session as user_session
from flask.ext.login import login_user, logout_user

import datetime

from phantomboreas.webservice import app, bcrypt, admin_required
from citations import api_get_citation, api_put_citation, api_get_citations_list, api_search_citation, datetime_option

from flask.ext.security import login_required

from phantomboreas.db.models import Base, DroneAuth, User
from phantomboreas.webservice import db_session
from phantomboreas.webservice.forms import UsernamePasswordForm, RegisterForm

import types

class CaptureAPI(MethodView):
	decorators = [login_required]
	def get(self, filename):
		return send_from_directory(app.config['IMAGE_STORE_PATH'], filename)


class DroneAuthAPI(MethodView):
	decorators = [login_required]
	def post(self):
		session = db_session()

		drone_auth = DroneAuth()

		session.add(drone_auth)
		session.commit()

		# response = make_response(drone_auth.key)

		# response.headers["Content-Disposition"] = "attachment; filename=key.txt"

		return jsonify({'key': drone_auth.key}), 200



class RegisterAPI(MethodView):
	def post(self):
		session     = db_session()
		form        = RegisterForm()

		if form.validate():
			user = User(username=form.username.data, password=bcrypt.generate_password_hash(form.password.data), is_admin=False)
			session.add(user)
			session.commit()

			login_user(user)

			return redirect(url_for('index'))
		else:
			user_session['register_form_errors'] = {
				'username': form.username.errors,
				'password': form.password.errors,
				'confirm' : form.confirm.errors
			}

		return redirect(url_for('signin'))


class UserAPI(MethodView):
	decorators = [login_required, admin_required]
	def get(self, user_id):
		session = db_session()

		if userId:
			u = session.query(User).filter_by(id=user_id)

			if u:
				return jsonify(u.first().toDict()), 200
			else:
				return '', 404

		else:
			users = []

			for u in session.query(User).all():
				users.append(u.toDict())

			return jsonify(users), 200



	def post(self):
		content = request.get_json()

		if not content.has_key('username') or not content.has_key('password'):
			return '', 400

		session = db_session()

		user = User(username=content.get('username'), password=bcrypt.generate_password_hash(content.get('password')), is_admin=False)

		session.add(user)
		session.commit()

		return jsonify(user.toDict()), 200

	def patch(self, user_id):
		content = request.get_json()

		session = db_session()
		user = session.query(User).filter_by(id=user_id)

		if not user:
			return '', 404

		# Admin shouldn't need to change user passwords or usernames
		# only allowing admins to make others users admins
		# Might be better to make this a seperate action
		if content.has_key('is_admin'):
			if isinstance(content.get('is_admin'), bool):
				user = user.first()
				user.is_admin = content.get('is_admin')
				session.commit()
				return '', 200
			else:
				return '', 400
		else:
			return '', 304


class CitationAPI(MethodView):
	decorators = [login_required]
	def get(self, citation_id):
		try:
			days_delta = int(request.args.get('days_delta')) if request.args.has_key('days_delta') else 99
			days_since = int(request.args.get('days_since')) if request.args.has_key('days_since') else 1
		except ValueError:
			return '', 400

		if citation_id is None: return api_get_citations_list(timedelta=datetime.timedelta(days=days_delta), since=(datetime.datetime.now() + datetime.timedelta(days=days_since)))
		# if citation_id is None: return api_get_citations_list()

		return api_get_citation(citation_id)

	def put(self, citation_id):
		return api_put_citation(citation_id)

class SearchAPI(MethodView):
    decorators = [login_required]
    def get(self):
        return api_search_citation()
