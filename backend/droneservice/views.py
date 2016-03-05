from flask import request
from flask.views import MethodView

from droneservice import process



class IndexView(MethodView):
    def get(self):
        return 'Hello from quadsquad193!', 200
