from flask import request
from flask.views import MethodView

from droneservice import process



class DroneImagesAPI(MethodView):
    def post(self):
        process.process(request)

        # Return HTTP 204 No Content
        return '', 204
