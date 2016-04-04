from flask import request, send_from_directory
from flask.views import MethodView

from phantomboreas.webservice import app



class CaptureAPI(MethodView):
    def get(self, filename):
        return send_from_directory(app.config['IMAGE_STORE_PATH'], filename)
