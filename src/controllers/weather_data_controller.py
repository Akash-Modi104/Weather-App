import logging
import json
import requests
from src import app
from flask import request, jsonify,session
from src.database.intialize_database import db
from src.entity.weather_details import WeatherData, weather_data_schema
from datetime import date, datetime

logger = logging.getLogger(__name__)


def get_weather_data(location):
    try:
        print(session)
        data = check_data(location)
        if not data["status"]:
            return jsonify(data), 404
        return jsonify(data), 200
    except Exception as e:
        logger.exception(e)
        return jsonify({"status": "not found"}), 500


def check_data(location):
    current_date = date.today()
    data = WeatherData.query.filter_by(location=location.lower()).first()
    if data:
        dumped_data = weather_data_schema.dump(data)
        created_at_date = datetime.fromisoformat(dumped_data['created_at']).date()

        if created_at_date != current_date:
            city_data = search_city(location)
            print(city_data)
            if city_data["status"]:
                weather_data = check_weather_data(city_data["Key"])
                if weather_data["status"]:
                    data.data = json.dumps(weather_data)
                    data.created_at = datetime.now()
                    db.session.commit()
                return weather_data
            return city_data
        else:
            return json.loads(dumped_data["data"])

    else:
        _data_ = search_city(location)
        _city_data = _data_
        if  _data_["status"]:
            _data_ = check_weather_data( _data_["Key"])
            if _data_["status"]:
                _data_["city"] = _city_data['EnglishName']
                _data_["country"] = _city_data['Country']['EnglishName']
                _data_["continent"] = _city_data['Region']['EnglishName']
                db_data_ =json.dumps(_data_)
                write_or_update_data(location.lower(),db_data_)

        return _data_


def write_or_update_data(location, _data):
    new_weather_data = WeatherData(location=location, data=_data)
    db.session.add(new_weather_data)
    db.session.commit()


def check_weather_data(location_key):
    api_key = app.config["api_key"]
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
    params = {
        'apikey': api_key
    }
    try:
        response = requests.get(url, params=params)
    except Exception as e:
        return {"status":False,"comment": "Max retries exceeded with url"}
    data = json.loads(response.text)[0]
    data["status"] = True
    return data


def search_city(location):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/search"
    api_key = app.config["api_key"]
    params = {
        'apikey': api_key,
        'q': location
    }
    response = requests.get(url, params=params)
    if response.status_code == 503:
        return {"status":False,"comment": "Max retries exceeded with url"}
    if response.text!= "[]":
        data = json.loads(response.text)[0]
        data["status"] = True
        return data
    return {"status":False,"comment": "city not found"}
