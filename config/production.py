
from .base import BaseConfig

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod.db'
    DEBUG = False
