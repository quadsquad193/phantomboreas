from phantomboreas.parkinglogservice.db import DB
from phantomboreas.db.models import Base



class TestParkingLogServiceDB:
    # DB should be able to configure a SQLite connection without error
    def test_db_config(self):
        db = DB()
        db.config({'db_url': 'sqlite://'})
        db.assert_config()
