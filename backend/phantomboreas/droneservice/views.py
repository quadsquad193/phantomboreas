from flask import request
from flask.views import MethodView



class IndexView(MethodView):
    def get(self):
        return 'Hello from quadsquad193!', 200
