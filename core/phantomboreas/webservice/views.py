from flask import request
from flask.views import MethodView
from flask import render_template

import process



class IndexView(MethodView):
    def get(self):
        return render_template('index.html'), 200
