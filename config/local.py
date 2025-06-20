
from .base import BaseConfig

class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///local.db'
    DEBUG = True
