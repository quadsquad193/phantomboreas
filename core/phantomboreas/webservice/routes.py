from phantomboreas.webservice import app, api, views, admin_required
from flask.ext.login import login_required


capture_view = login_required(api.CaptureAPI.as_view('capture'))
app.add_url_rule('/assets/capture/<filename>', view_func=capture_view)

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