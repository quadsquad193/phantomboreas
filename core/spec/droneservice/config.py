# Statement for enabling the development environment
DEBUG = True

TESTING = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

IMAGE_STORE_PATH = os.path.join(BASE_DIR, 'imgstore')

REDIS_CONN = {
    'host': 'localhost',
    'port': 6379,
    'db_index': 1
}

REDIS_MQ = {
    'openalpr_queue':           'openalpr:queue',
}
