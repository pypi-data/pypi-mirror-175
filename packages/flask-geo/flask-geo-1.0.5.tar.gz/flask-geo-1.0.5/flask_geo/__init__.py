from flask import Flask
from importlib import import_module

from .domain import ICountryRepository, ICityRepository


class FlaskGeo:

    def __init__(self, country_repository: ICountryRepository, city_repository: ICityRepository, app: Flask = None):
        self.city_repository = city_repository
        self.country_repository = country_repository
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        app.geo = self
        import_module('flask_geo.api').init_app(app)
