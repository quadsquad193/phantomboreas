from droneservice import app
import os
import datetime
import binascii



IMAGE_STORE_PATH = app.config['IMAGE_STORE_PATH']



def process(request):
    f           = request.files['image']
    timestamp   = datetime.datetime.utcnow().strftime("%s")
    # timestamp   = request.form['timestamp']
    # latitude    = request.form['latitude']
    # longitude   = request.form['longitude']

    image_ext   = f.filename.rsplit('.', 1)[1]
    filename    = timestamp + '-' + random_hash() + '.' + image_ext

    f.save(os.path.join(IMAGE_STORE_PATH, filename))

    # TODO: enqueue onto MQ service

def random_hash():
    return binascii.b2a_hex(os.urandom(3))
