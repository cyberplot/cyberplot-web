class BaseConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///cyberplot.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret"