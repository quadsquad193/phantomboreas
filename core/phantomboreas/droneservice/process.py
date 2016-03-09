from flask import request
import os
import binascii
import pickle

from phantomboreas.droneservice import app, redis_client



IMAGE_STORE_PATH    = app.config['IMAGE_STORE_PATH']
OPENALPR_QUEUE_KEY  = app.config['REDIS_MQ']['openalpr_queue']



def process(request):
    f                   = request.files['image']
    timestamp           = request.form.get('timestamp', type=int)
    latitude            = request.form.get('latitude',  type=float)
    longitude           = request.form.get('longitude', type=float)

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
