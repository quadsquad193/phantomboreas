import pytest
from pytest_dbfixtures import factories

import pickle
import os
import openalpr

import config
from openalprservice.worker import Worker, UnloadableALPR


redis_conf = {
    'host':             config.REDIS_CONN['host'],
    'port':             config.REDIS_CONN['port'],
    'db_index':         1,
    'queue_key':        config.REDIS_MQ['openalpr_queue'],
    'processing_key':   config.REDIS_MQ['openalpr_processing'],
    'results_key':      config.REDIS_MQ['parkinglog_queue']
}

openalpr_conf = {
    'country':      config.OPENALPR['country'],
    'region':       config.OPENALPR['region'],
    'config_file':  config.OPENALPR['config_file'],
    'runtime_dir':  config.OPENALPR['runtime_dir']
}

redis_proc = factories.redis_proc()
redisdb = factories.redisdb('redis_proc', db=1)

image = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.jpg'))
TEST_IMAGE_STREAM = image.read()
image.close()



class TestWorker:
    # The UnloadableALPR class should be a proxy container for openalpr.Alpr
    # instances
    def test_UnloadableALPR_is_subclass(self):
        alpr = UnloadableALPR(openalpr_conf['country'], openalpr_conf['config_file'], openalpr_conf['runtime_dir'])

        assert isinstance(alpr, openalpr.Alpr)

    # Unconfigured workers should raise an exception when called to run
    def test_unconfigured_worker(self):
        worker = Worker()

        with pytest.raises(RuntimeError):
            worker.run()

    # Test the Redis fixture
    def test_redis(self, redisdb):
        assert redisdb.echo('Hello, World!') == 'Hello, World!'

    # Ensure basic functionality of the worker process
    def test_process_image_and_result(self, redisdb):
        worker = Worker()
        worker.config(redis_conf, openalpr_conf)

        # Stub the worker's Redis client
        worker.redis_client = redisdb

        pickled_payload = pickle.dumps({
            'filename':         'test.jpg',
            'latitude':         38.537002,
            'longitude':        -121.754725,
            'timestamp':        1457395109,
            'image':            TEST_IMAGE_STREAM
        })

        redisdb.lpush(redis_conf['queue_key'], pickled_payload)

        worker.process_image()

        pickled_result_payload = redisdb.rpop(redis_conf['results_key'])

        # The worker, given that OpenALPR had results to report, should place
        # an augmented "results" payload into Redis
        assert pickled_result_payload is not None

        result_payload = pickle.loads(pickled_result_payload)

        # The results payload should contain any preexisting data
        assert result_payload['filename']   == 'test.jpg'
        assert result_payload['latitude']   == 38.537002
        assert result_payload['longitude']  == -121.754725
        assert result_payload['timestamp']  == 1457395109

        openalpr_results = result_payload['openalpr_results']

        # We assume that our test image had one plate detected
        assert len(openalpr_results) == 1

        first_plate_openalpr_results = openalpr_results[0]

        # Ensure OpenALPR gives a set of plate coordinates
        assert first_plate_openalpr_results['coordinates'] is not None

        first_candidates_openalpr_results = first_plate_openalpr_results['candidates']

        # Check the validity of the candidates.
        assert len(first_candidates_openalpr_results) > 0
        assert '420LIM0' in map(lambda x: x['plate'], first_candidates_openalpr_results)
