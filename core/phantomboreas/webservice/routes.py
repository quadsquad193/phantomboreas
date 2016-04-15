from phantomboreas.webservice import app, api, views


app.add_url_rule('/assets/capture/<filename>', view_func=api.CaptureAPI.as_view('capture'))
app.add_url_rule('/drone_auth', view_func=api.DroneAuthAPI.as_view('drone_auth'))
app.add_url_rule('/', view_func=views.IndexView.as_view('index'))
app.add_url_rule('/signin', view_func=views.SigninView.as_view('signin'))
app.add_url_rule('/signout', view_func=views.UserLogoutView.as_view('signout'))
app.add_url_rule('/test_users', view_func=api.TestUsersAPI.as_view('test_users'))
