import sqlalchemy

from parkinglogservice import utils



class Logger(object):
    def __init__(self):
        self.configured = False
        self.db_conn    = None

    def config(self, db_conf):
        self.db_conn = None

        self.configured = True

    def assert_config(self):
        if not self.configured: raise RuntimeError("Logger not yet configured with config() method.")

    def process(self, payload):
        # TODO: do stuff with the OpenALPR results

        utils.debug_print_results(payload['openalpr_results'])
