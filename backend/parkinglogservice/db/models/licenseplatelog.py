from sqlalchemy import Column, String

from base import Base



class LicensePlateLog(Base):
    __tablename__ = 'license_plate_log'

    id = Column(String, primary_key=True)
