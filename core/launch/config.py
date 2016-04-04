import secrets

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_DEFINITION = 'mysql://' + secrets.DB_USER + ':' + secrets.DB_PASSWORD + '@localhost'
SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_DEFINITION + '/' + 'app'
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = secrets.CSRF_SESSION_KEY

# Secret key for signing cookies
SECRET_KEY = secrets.SECRET_KEY

IMAGE_STORE_PATH = os.path.join(BASE_DIR, 'imgstore')

REDIS_CONN = {
    'host': 'localhost',
    'port': 6379,
    'db_index': 0
}

REDIS_MQ = {
    'openalpr_queue':           'openalpr:queue',
    'openalpr_processing':      'openalpr:processing',
    'parkinglog_queue':         'parkinglog:queue',
    'parkinglog_processing':    'parkinglog:processing'
}

OPENALPR = {
    'country': 'us',
    'region': 'ca',
    'config_file': '/etc/openalpr/openalpr.conf',
    'runtime_dir': '/usr/share/openalpr/runtime_data'
}
