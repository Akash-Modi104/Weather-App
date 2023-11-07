import logging
import pathlib
from typing import Any

from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

from configs.log_config import setup_logger
from src.database.intialize_database import create_table_not_exits

app = Flask(__name__)
logger = logging.getLogger(__name__)


def create_app(env: str) -> Any:
    try:
        CORS(app=app)
        project_path = pathlib.Path(__file__).parent.parent
        os.makedirs(pathlib.Path(project_path).joinpath("logs"), exist_ok=True)
        os.makedirs(pathlib.Path(project_path).joinpath("database"), exist_ok=True)
        setup_logger(env)
        env_path = os.path.join(pathlib.Path(__file__).parent.parent, '.env')
        load_dotenv(dotenv_path=env_path)
        app.config["api_key"] = os.getenv('WEATHER_API_KEY')
        with app.app_context():
            file_path = os.path.join(pathlib.Path(__file__).parent.parent,
                                     f"{os.getenv('DB_NAME')}.sqlite")
            app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{file_path}'
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            app.secret_key = os.getenv('SECRET_KEY')
            create_table_not_exits(app)
            from src.routes import all_routes
            logger.info("####### app started #########")
            return app
    except Exception as e:
        logger.exception(e)
        return None
