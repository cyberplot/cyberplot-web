from flask import Flask

def create_app(app_name="CYBERPLOT"):
    app = Flask(app_name)
    app.config.from_object("cyberplot.config.BaseConfig")

    from cyberplot.api import api
    app.register_blueprint(api, url_prefix="/api")

    from cyberplot.models import db
    db.init_app(app)

    return app