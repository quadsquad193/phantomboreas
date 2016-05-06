from phantomboreas.webservice import app, bcrypt, admin_required

from flask import request
from flask.views import MethodView
from flask import render_template

from flask import redirect, url_for

from flask.ext.login import login_user, logout_user

# import sqlalchemy as sa
# from sqlalchemy import orm
# from sqlalchemy import create_engine

from phantomboreas.db.models import Base, CaptureLog, PlateLog, CandidateLog, User
from phantomboreas.webservice import db_session, bcrypt
from phantomboreas.webservice.forms import UsernamePasswordForm, RegisterForm
from flask.ext.security import login_required
from flask.ext.login import current_user
import process



class IndexView(MethodView):
    decorators = [login_required]
    def get(self):
    	session = db_session()

    	_capture_list = session.query(CaptureLog).all()
    	capture_list = []

    	for capture in _capture_list:
    		#Get necessary capture info and put it in json format
    		c = {'filename': capture.filename, 'plates': []}

    		#Add necessary information about plates and candidates
    		for plate in capture.plates:
    			p = {'id': plate.id, 'candidates': []}

    			for candidate in plate.candidates:
    				p['candidates'].append({'license_plate': candidate.license_plate, 'confidence': candidate.confidence})

    			c['plates'].append(p)

    		capture_list.append(c)

        return render_template('index.html', capture_list=capture_list, current_user=current_user), 200

class CitationsView(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('citations.html', current_user=current_user), 200

class UserLogoutView(MethodView):
    decorators = [login_required]
    def get(self):
        logout_user()

        return redirect(url_for('index'))

class SigninView(MethodView):
    def get(self):
        signin_form = UsernamePasswordForm()
        register_form = RegisterForm()

        return render_template('signin.html', signin_form=signin_form, register_form=register_form)

    def post(self):
        session = db_session()
        form = UsernamePasswordForm()

        user = session.query(User).filter_by(username=form.username.data).first()
        if form.validate() and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)

            return redirect(url_for('index'))
        else:
            return redirect(url_for('signin'))


class SummaryView(MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('summary.html', current_user=current_user)

class AdminView(MethodView):
    decorators = [login_required, admin_required]
    def get(self):
        session = db_session()
        users = []

        for u in session.query(User).all():
            users.append(u.toDict())

        return render_template('admin.html', users=users, current_user=current_user), 200
