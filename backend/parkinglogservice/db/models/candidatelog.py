from sqlalchemy import Column, String, Boolean, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from base import Base



class CandidateLog(Base):
    __tablename__ = 'candidate_log'

    id = Column(Integer, primary_key=True)
    license_plate = Column(String)
    verified = Column(Boolean, default=False)
    confidence = Column(Float)
    capture_id = Column(Integer, ForeignKey('capture_log.id'))
    capture = relationship("CaptureLog", back_populates="candidates")