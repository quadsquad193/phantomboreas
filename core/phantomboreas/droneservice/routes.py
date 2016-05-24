from phantomboreas.droneservice import app, api, views

app.add_url_rule('/droneimages', view_func=api.DroneImagesAPI.as_view('droneimages'))
app.add_url_rule('/', view_func=views.IndexView.as_view('index'))
app.add_url_rule('/authenticate_drone', view_func=api.AuthenticateDroneAPI.as_view('authenticate_drone'))