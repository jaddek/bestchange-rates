import os
from dotenv import load_dotenv
from flask import Flask

from containers import Container
from views import index
from commands import *

def create_app(test_config=None) -> Flask:
    load_dotenv()
    container = Container()
    container.wire(modules=[__name__])

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.container = container

    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.add_url_rule("/", view_func=index)
    app.add_url_rule("/bc.xml", view_func=index)

    app.cli.add_command(create_user)

    return app
