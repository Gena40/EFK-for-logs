from flask import Flask
from .routes import api


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    return app


def run_app(*args, **kwargs):
    app = create_app()
    app.run(*args, **kwargs)


if __name__ == '__main__':
    run_app()