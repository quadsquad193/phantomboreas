import pytest
from pytest_dbfixtures import factories

import pickle

from phantomboreas.parkinglogservice.worker import Worker
from phantomboreas.parkinglogservice.db import DB
from phantomboreas.parkinglogservice.logger import Logger
from phantomboreas.parkinglogservice.arbiter import Arbiter



redis_conf = {
    'host':             'localhost',
    'port':             '?',
    'db_index':         1,
    'queue_key':        'test:parkinglog:queue',
    'processing_key':   'test:parkinglog:processing'
}

redis_proc = factories.redis_proc(host=redis_conf['host'], port=redis_conf['port'])
redisdb = factories.redisdb('redis_proc', db=1)



class TestParkingLogServiceWorker:
    # Unconfigured workers should raise an exception when called to run
    def test_unconfigured_worker(self):
        db = DB()
        logger = Logger(db)
        arbiter = Arbiter(db)
        worker = Worker(logger, arbiter)

        with pytest.raises(RuntimeError):
            worker.run()

    # Configured workers with unconfigured dependencies should raise an
    # exception when called to run
    def test_configured_worker_with_unconfigured_logger(self):
        db = DB()
        logger = Logger(db)
        arbiter = Arbiter(db)
        worker = Worker(logger, arbiter)

        worker.config(redis_conf)

        with pytest.raises(RuntimeError):
            worker.run()

    # Test the Redis fixture
    def test_redis(self, redisdb):
        assert redisdb.echo('Hello, World!') == 'Hello, World!'

    # Show that the worker can dequeue and unpickle payloads from a Redis queue
    def test_worker_redis(self, monkeypatch, redisdb):
        db = DB()
        logger = Logger(db)
        arbiter = Arbiter(db)
        worker = Worker(logger, arbiter)

        worker.config(redis_conf)

        payload = {'openalpr_results': {'4': 2, '0': 'blaze it'}}
        def logger_process(p):
            assert all(p[k] == v for k, v in payload.iteritems())
            return True
        def arbiter_process(c):
            assert c

        monkeypatch.setattr(worker, 'redis_client', redisdb)
        monkeypatch.setattr(db, 'assert_config', lambda: None)
        monkeypatch.setattr(logger, 'assert_config', lambda: None)
        monkeypatch.setattr(arbiter, 'assert_config', lambda: None)
        monkeypatch.setattr(logger, 'process', logger_process)
        monkeypatch.setattr(arbiter, 'process', arbiter_process)

        redisdb.lpush(redis_conf['queue_key'], pickle.dumps(payload))

        worker.process_alpr_captures()
