from flask import Flask
from flask_cors import CORS

def create_app(app_name="CYBERPLOT"):
    app = Flask(app_name)
    app.config.from_object("cyberplot.config.BaseConfig")

    cors = CORS(app, resources={ r"/api/*": { "origins": "*" } })

    from cyberplot.api import api
    app.register_blueprint(api, url_prefix="/api")

    from cyberplot.models import db
    db.init_app(app)

    return app