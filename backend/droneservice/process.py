from flask import request
from droneservice import app, redis_client
import os
import binascii
import pickle



IMAGE_STORE_PATH    = app.config['IMAGE_STORE_PATH']
OPENALPR_QUEUE_KEY  = app.config['REDIS_MQ']['openalpr_queue']



def process(request):
    f                   = request.files['image']
    timestamp           = int(request.form['timestamp'])
    latitude            = float(request.form['latitude'])
    longitude           = float(request.form['longitude'])

    image_ext   = f.filename.rsplit('.', 1)[1]
    filename    = str(timestamp) + '-' + random_hash() + '.' + image_ext

    payload = {
        'filename':         filename,
        'latitude':         latitude,
        'longitude':        longitude,
        'timestamp':        timestamp,
        'image':            f.stream.read()
    }

    redis_client.lpush(OPENALPR_QUEUE_KEY, pickle.dumps(payload))
    f.close()

def random_hash():
    return binascii.b2a_hex(os.urandom(3))
