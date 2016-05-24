from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from base import Base
from citationlog import CitationLog, evidence_table



class PlateLog(Base):
    __tablename__ = 'plate_log'

    id = Column(Integer, primary_key=True)

    # Cartesian points, in clockwise-order, starting from the top-left "corner"
    # of the bounding polygon
    upper_left_x    = Column(Integer)
    upper_left_y    = Column(Integer)
    upper_right_x   = Column(Integer)
    upper_right_y   = Column(Integer)
    lower_right_x   = Column(Integer)
    lower_right_y   = Column(Integer)
    lower_left_x    = Column(Integer)
    lower_left_y    = Column(Integer)

    capture_id = Column(Integer, ForeignKey('capture_log.id'))
    capture = relationship("CaptureLog", back_populates="plates")
    candidates = relationship("CandidateLog", back_populates="plate")

    citation = relationship("CitationLog", uselist=False, back_populates="plate")
