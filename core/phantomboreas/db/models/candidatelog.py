from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship

from base import Base



class CandidateLog(Base):
    __tablename__ = 'candidate_log'

    id = Column(Integer, primary_key=True)

    license_plate   = Column(String(32))
    confidence      = Column(Float)

    plate_id = Column(Integer, ForeignKey('plate_log.id'))
    plate = relationship("PlateLog", back_populates="candidates")
