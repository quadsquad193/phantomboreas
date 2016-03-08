import pytest

import sqlalchemy

from db.models import Base



class Testmodels:
    # Ensure all models registered through the Base object can have each
    # respective table created
    def test_models(self):
            db_engine = sqlalchemy.create_engine('sqlite://')
            Base.metadata.create_all(db_engine)
