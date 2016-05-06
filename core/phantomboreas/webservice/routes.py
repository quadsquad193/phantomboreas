from phantomboreas.webservice import app, api, views, admin_required
from flask.ext.login import login_required


capture_api_view = login_required(api.CaptureAPI.as_view('capture'))
app.add_url_rule('/assets/capture/<filename>', view_func=capture_api_view)

drone_auth_view = login_required(api.DroneAuthAPI.as_view('drone_auth'))
app.add_url_rule('/drone_auth', view_func=drone_auth_view)

index_view = login_required(views.IndexView.as_view('index'))
app.add_url_rule('/', view_func=index_view)

app.add_url_rule('/signin', view_func=views.SigninView.as_view('signin'))
app.add_url_rule('/signout', view_func=views.UserLogoutView.as_view('signout'))

admin_view = admin_required(login_required(views.AdminView.as_view('admin')))
app.add_url_rule('/admin', view_func=admin_view)

user_view = admin_required(login_required(api.UserAPI.as_view('users')))
app.add_url_rule('/users', view_func=user_view, methods=['GET', 'POST'])
app.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET', 'PATCH'])

citation_api_view   = login_required(api.CitationAPI.as_view('citation'))
search_api_view     = login_required(api.SearchAPI.as_view('search'))
citations_view      = login_required(views.CitationsView.as_view('citations'))

summary_view = login_required(views.SummaryView.as_view('summary'))
app.add_url_rule('/summary', view_func=summary_view)

app.add_url_rule('/api/citation/search/', view_func=search_api_view)
app.add_url_rule('/api/citation/', defaults={'citation_id': None}, methods=['GET'], view_func=citation_api_view)
app.add_url_rule('/api/citation/<int:citation_id>', methods=['GET', 'PUT'], view_func=citation_api_view)
app.add_url_rule('/citations/', view_func=citations_view)
app.add_url_rule('/register', view_func=api.RegisterAPI.as_view('register'))
