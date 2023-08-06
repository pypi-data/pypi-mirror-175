from flask import Flask
from importlib import import_module
from flask_geo import FlaskGeo
from flask_geo.domain import ICountryRepository, ICityRepository

from .views import bp


class SignsCalculator:

    def __init__(self, country_repository: ICountryRepository, city_repository: ICityRepository, app: Flask = None) -> None:
        self.__country_repository = country_repository
        self.__city_repository = city_repository
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        app.signs_calculator = self
        FlaskGeo(self.__country_repository, self.__city_repository, app)
        app.register_blueprint(bp)
