from phantomboreas.webservice import app, api, views



capture_api_view    = api.CaptureAPI.as_view('capture')
citation_api_view   = api.CitationAPI.as_view('citation')
index_view          = views.IndexView.as_view('index')

app.add_url_rule('/assets/capture/<filename>', view_func=capture_api_view)
app.add_url_rule('/api/citation/', defaults={'citation_id': None}, methods=['GET'], view_func=citation_api_view)
app.add_url_rule('/api/citation/<int:citation_id>', methods=['GET', 'PUT'], view_func=citation_api_view)
app.add_url_rule('/', view_func=index_view)
