from sqlalchemy import Column, Integer, String, Boolean
from flask.ext.login import UserMixin
from base import Base


class User(Base, UserMixin):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	username = Column(String(32), nullable=False, unique=True)
	password = Column(String(128), nullable=False)
	is_admin = Column(Boolean, default=False)


	def __init__(self, username, password, is_admin=False):
		self.username = username
		self.password = password
		self.is_admin = is_admin

	def __repr__(self):
		return "<User(username='%s', id_admin='%s')>" % (self.username, self.is_admin)

	# def is_correct_password(self, plaintext):
	# 	if bcrypt.check_password_hash(self.password, plaintext):
	# 		return True

	# 	return False