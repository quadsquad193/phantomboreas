import redis
import pickle
import os
import binascii



class Worker(object):
    def __init__(self):
        self.configured     = False
        self.redis_client   = None
        self.queue_key      = None
        self.processing_key = None

    def config(self, redis_conf):
        self.redis_client   = redis.StrictRedis(host=redis_conf['host'], port=redis_conf['port'], db=0)
        self.queue_key      = redis_conf['queue_key']
        self.processing_key = redis_conf['processing_key'] + ':' + random_hash()

        self.configured = True

    def run(self):
        if not self.configured: raise RuntimeError("Worker not yet configured with config() method.")

        while(True):
            self.process_alpr()

    def process_alpr(self):
        pickled_payload = self.redis_client.brpoplpush(self.queue_key, self.processing_key)
        payload = pickle.loads(pickled_payload)

        # TODO: do stuff with the OpenALPR results

        debug_print_results(payload['openalpr_results'])

        self.redis_client.lpop(self.processing_key)



def random_hash():
    return binascii.b2a_hex(os.urandom(3))

def debug_print_results(results):
        # Uncomment to see the full results structure
        # import pprint
        # pprint.pprint(results)

        i = 0
        for plate in results:
            i += 1
            print("Plate #%d" % i)
            print("   %12s %12s" % ("Plate", "Confidence"))
            for candidate in plate['candidates']:
                prefix = "-"
                if candidate['matches_template']:
                    prefix = "*"

                print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))
