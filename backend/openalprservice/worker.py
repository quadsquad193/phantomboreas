import redis
import openalpr
import pickle
import os
import binascii



class UnloadableALPR(openalpr.Alpr):
    def __init__(self, *args, **kwargs):
        # openalpr.Alpr is an old-style class
        openalpr.Alpr.__init__(self, *args, **kwargs)

    def __enter__(self):
        pass

    def __exit__(self, etype, value, traceback):
        self.unload()

class Worker(object):
    def __init__(self):
        self.configured     = False
        self.redis_client   = None
        self.queue_key      = None
        self.processing_key = None

    def config(self, redis_conf, openalpr_conf):
        self.redis_client   = redis.StrictRedis(host=redis_conf['host'], port=redis_conf['port'], db=0)
        self.queue_key      = redis_conf['queue_key']
        self.processing_key = redis_conf['processing_key'] + ':' + random_hash()
        self.results_key    = redis_conf['results_key']

        self.alpr           = UnloadableALPR(openalpr_conf['country'], openalpr_conf['config_file'], openalpr_conf['runtime_dir'])
        self.alpr.set_top_n(5)
        self.alpr.set_default_region(openalpr_conf['region'])

        self.configured = True

    def run(self):
        if not self.configured: raise RuntimeError("Worker not yet configured with config() method.")

        with self.alpr:
            while(True):
                self.process_image()

    def process_image(self):
        pickled_payload = self.redis_client.brpoplpush(self.queue_key, self.processing_key)
        payload = pickle.loads(pickled_payload)

        image_bytes = payload['image']
        results = self.alpr.recognize_array(image_bytes)

        self.redis_client.lpop(self.processing_key)

        if results['results']:
            self.process_result(payload, results['results'])

    def process_result(self, payload, result):
        payload['openalpr_results'] = result
        pickled_payload = pickle.dumps(payload)

        self.redis_client.lpush(self.results_key, pickled_payload)



def random_hash():
    return binascii.b2a_hex(os.urandom(3))
