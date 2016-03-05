from sqlalchemy import Column, String, Integer, LargeBinary, Float, Date
from sqlalchemy.orm import relationship

from base import Base

class CaptureLog(Base):
	__tablename__ = 'capture_log'

	id = Column(Integer, primary_key=True)
	image = Column(LargeBinary)
	filename = Column(String)
	latitude = Column(Float)
	longitude = Column(Float)
	timestamp = Column(Date)
	candidates = relationship("CandidateLog", back_populates="capture")
