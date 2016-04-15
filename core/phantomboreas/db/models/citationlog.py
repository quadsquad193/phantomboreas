from sqlalchemy import Table, Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base



evidence_table = Table('evidence_table', Base.metadata,
    Column('citation_id', Integer, ForeignKey('citation_log.id')),
    Column('evidence_id', Integer, ForeignKey('plate_log.id'))
)

class CitationLog(Base):
    __tablename__ = 'citation_log'

    id = Column(Integer, primary_key=True)

    verified    = Column(Boolean, default=False)
    dismissed   = Column(Boolean, default=False)
    hidden      = Column(Boolean, default=False)

    plate_id    = Column(Integer, ForeignKey('plate_log.id'))

    plate       = relationship("PlateLog", foreign_keys=[plate_id], back_populates="citation")
    evidence    = relationship("PlateLog", secondary=evidence_table)

    # See http://docs.sqlalchemy.org/en/latest/orm/self_referential.html
    delegate_id = Column(Integer, ForeignKey('citation_log.id'))
    delegations = relationship("CitationLog", foreign_keys=[delegate_id], backref=backref('delegate', remote_side=[id]))
