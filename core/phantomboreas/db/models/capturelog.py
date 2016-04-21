from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.orm import relationship

from base import Base



class CaptureLog(Base):
    __tablename__ = 'capture_log'

    id = Column(Integer, primary_key=True)

    filepath        = Column(String(256))
    filename        = Column(String(256))
    latitude        = Column(Numeric(precision=10, scale=7))
    longitude       = Column(Numeric(precision=10, scale=7))
    timestamp       = Column(DateTime)

    plates = relationship("PlateLog", back_populates="capture")
