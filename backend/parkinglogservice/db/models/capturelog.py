from sqlalchemy import Column, Integer, LargeBinary, String, Float, Date
from sqlalchemy.orm import relationship

from base import Base



class CaptureLog(Base):
    __tablename__ = 'capture_log'

    id = Column(Integer, primary_key=True)

    image           = Column(LargeBinary)
    filename        = Column(String)
    latitude        = Column(Float)
    longitude       = Column(Float)
    timestamp       = Column(Date)

    plates = relationship("PlateLog", back_populates="capture")
