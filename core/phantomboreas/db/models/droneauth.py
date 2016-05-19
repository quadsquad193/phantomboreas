from sqlalchemy import Column, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
from base import Base
import config
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI


# from phantomboreas.droneservice import app

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class DroneAuth(Base):
    __tablename__ = "drone_auth"

    key = Column(String(64), primary_key=True)

    def __init__(self):
        self.key = uuid.uuid4()

    def generate_auth_token(self, expiration = 604800):
        s = Serializer(SECRET_KEY, expires_in = expiration)
        return s.dumps({ 'key': self.key })

    @staticmethod
    def verify_auth_token(token):
        if token == None:
            return None

        s = Serializer(SECRET_KEY)

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token

        db_session = sessionmaker()
        db_engine = create_engine(SQLALCHEMY_DATABASE_URI)
        db_session.configure(bind=db_engine)
        session = db_session()

        drone_auth = session.query(DroneAuth).get(data['key'])
        return drone_auth
