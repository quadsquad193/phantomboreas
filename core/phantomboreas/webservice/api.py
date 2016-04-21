from flask import request, send_from_directory
from flask.views import MethodView

import datetime

from phantomboreas.webservice import app
from citations import api_get_citation, api_put_citation, api_get_citations_list



class CaptureAPI(MethodView):
    def get(self, filename):
        return send_from_directory(app.config['IMAGE_STORE_PATH'], filename)

class CitationAPI(MethodView):
    def get(self, citation_id):
        if citation_id is None: return api_get_citations_list()

        return api_get_citation(citation_id)

    def put(self, citation_id):
        return api_put_citation(citation_id)
