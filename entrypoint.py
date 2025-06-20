
from flask import Flask
from config.local import LocalConfig
from extensions import db
from routes import asset_bp, check_bp

def create_app(config_class=LocalConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(asset_bp, url_prefix="/api")
    app.register_blueprint(check_bp, url_prefix="/api")

    return app

app = create_app()

