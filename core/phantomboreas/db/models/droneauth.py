from sqlalchemy import Column, String
import uuid
from base import Base


class DroneAuth(Base):
	__tablename__ = "drone_auth"

	key = Column(String(64), primary_key=True)

	def __init__(self):
		self.key = uuid.uuid4()