from flask import Flask
from config import config_options
from dotenv import load_dotenv
from flask_mongoengine import MongoEngine

dbmongo = MongoEngine()


def create_app(config_name):
    load_dotenv('.env')
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])
    print(f"MONGO_URI: {app.config['MONGO_URI']}")
    dbmongo.init_app(app)
    print(app.config)

    # Registrar Blueprints
    from .blueprints import product_blueprint, category_blueprint

    app.register_blueprint(product_blueprint)
    app.register_blueprint(category_blueprint)

    return app
