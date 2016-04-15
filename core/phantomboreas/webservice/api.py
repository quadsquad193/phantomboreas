from flask import request, send_from_directory
from flask.views import MethodView

import datetime

from phantomboreas.webservice import app
from citations import api_get_interval



class CaptureAPI(MethodView):
    def get(self, filename):
        return send_from_directory(app.config['IMAGE_STORE_PATH'], filename)

class CitationAPI(MethodView):
    def get(self):
        return api_get_interval()
