from droneservice import app, api

app.add_url_rule('/droneimages', view_func=api.DroneImagesAPI.as_view('droneimages'))
