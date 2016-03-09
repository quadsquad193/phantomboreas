import pytest
from pytest_dbfixtures import factories

import os
from StringIO import StringIO
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request
import pickle

from phantomboreas.droneservice import app, redis_client, process



redis_proc = factories.redis_proc(host=app.config['REDIS_CONN']['host'], port=app.config['REDIS_CONN']['port'])
redisdb = factories.redisdb('redis_proc', db=app.config['REDIS_CONN']['db_index'])



class TestDroneServiceApp:
    def test_api_route_droneimages(self, monkeypatch):
        def receive_payload(payload):
            assert payload is not None

        monkeypatch.setattr(process, 'process', receive_payload)

        response = app.test_client().post(
            '/droneimages',
            buffered=True,
            content_type='multipart/form-data',
            data=dict(
                image=(StringIO('Hello, World!'), 'test.jpg'),
                latitude='38.537002',
                longitude='-121.754725',
                timestamp='1457395109'
            )
        )

        assert response.status_code == 204

    def test_process(self, monkeypatch, redisdb):
        monkeypatch.setattr('phantomboreas.droneservice.redis_client', redisdb)
        monkeypatch.setattr(process, 'OPENALPR_QUEUE_KEY', 'test:' + process.OPENALPR_QUEUE_KEY)

        env = EnvironBuilder(
            method='POST',
            data=dict(
                image=(StringIO('Hello, World!'), 'test.jpg'),
                latitude='38.537002',
                longitude='-121.754725',
                timestamp='1457395109'
            )
        ).get_environ()

        process.process(Request(env))

        pickled_payload = redisdb.rpop(process.OPENALPR_QUEUE_KEY)

        assert pickled_payload is not None

        payload = pickle.loads(pickled_payload)

        assert '1457395109'         in payload['filename']
        assert payload['latitude']  == 38.537002
        assert payload['longitude'] == -121.754725
        assert payload['timestamp'] == 1457395109
        assert payload['image']     == 'Hello, World!'
