import redis
import pickle
import os
import binascii



class Worker(object):
    def __init__(self, logger):
        self.configured     = False
        self.redis_client   = None
        self.queue_key      = None
        self.processing_key = None

        self.logger = logger

    def config(self, redis_conf):
        self.redis_client   = redis.StrictRedis(host=redis_conf['host'], port=redis_conf['port'], db=redis_conf['db_index'])
        self.queue_key      = redis_conf['queue_key']
        self.processing_key = redis_conf['processing_key'] + ':' + random_hash()

        self.configured = True

    def assert_config(self):
        if not self.configured: raise RuntimeError("Worker not yet configured with config() method.")

        self.logger.assert_config()

    def run(self):
        self.assert_config()

        while(True):
            self.process_alpr()

    def process_alpr(self):
        pickled_payload = self.redis_client.brpoplpush(self.queue_key, self.processing_key)
        payload = pickle.loads(pickled_payload)

        # Assign a random hash to uniquely identify a set of one or more
        # recognized plates
        payload['process_hash'] = random_hash()

        # Give to Logger instance to handle
        self.logger.process(payload)

        self.redis_client.lpop(self.processing_key)



def random_hash():
    return binascii.b2a_hex(os.urandom(3))
