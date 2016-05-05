from phantomboreas.droneservice import app
from StringIO import StringIO

from config import BASE_DIR

with open(BASE_DIR+'/imgtest/img1.jpg', 'rb') as img1:
	img1StringIO = StringIO(img1.read())

	response = app.test_client().post('/droneimages',
	                         content_type='multipart/form-data',
	                         data={'timestamp': '1461882228', 'latitude': '127.34556', 'longitude': '-50',
	                         'f': (img1StringIO, 'img1.jpg')},
	                         follow_redirects=True)
	print(response)

 