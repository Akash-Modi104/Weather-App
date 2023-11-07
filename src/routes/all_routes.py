from flask import current_app as app, session
from src.controllers.weather_data_controller import get_weather_data
from src.controllers.user_controller import add_user, login, logout
from src.middleware.middleware import login_required


@app.route('/api/login', methods=["POST"])
def login_user():
    return login()


@app.route("/api/signup", methods=["POST"])
def signup():
    return add_user()


@app.route('/api/logout/<username>', methods=['GET'])
def logout_user(username):
    return logout(username)



@app.route("/api/weather/<location>", methods=["GET"])
def weather_data(location):
    return get_weather_data(location)
