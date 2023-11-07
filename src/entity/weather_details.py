from datetime import datetime
from src.database.intialize_database import db, ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class WeatherData(db.Model):
    u_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(100),nullable=False)
    data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self,location, data):
        self.location = location
        self.data = data

class WeatherDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WeatherData

weather_data_schema = WeatherDataSchema()