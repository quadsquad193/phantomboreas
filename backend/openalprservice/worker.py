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
    # redis_host, redis_port, queue_key, processing_key, openalpr_config):
        self.redis_client   = redis.StrictRedis(host=redis_conf['host'], port=redis_conf['port'], db=0)
        self.queue_key      = redis_conf['queue_key']
        self.processing_key = redis_conf['processing_key'] + ':' + random_hash()

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

        debug_print_results(results)

        self.redis_client.rpop(self.processing_key)



def random_hash():
    return binascii.b2a_hex(os.urandom(3))

def debug_print_results(results):
        # Uncomment to see the full results structure
        # import pprint
        # pprint.pprint(results)

        print("Image size: %dx%d" %(results['img_width'], results['img_height']))
        print("Processing Time: %f" % results['processing_time_ms'])

        i = 0
        for plate in results['results']:
            i += 1
            print("Plate #%d" % i)
            print("   %12s %12s" % ("Plate", "Confidence"))
            for candidate in plate['candidates']:
                prefix = "-"
                if candidate['matches_template']:
                    prefix = "*"

                print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))
