# app/__init__.py
from flask import Flask
from flask_restful import Api


def create_app():
    app = Flask(__name__)

    api = Api(app)

    from flask_app.app.resources.hello_world import HelloWorld
    from flask_app.app.resources.movies import Movies
    from flask_app.app.resources.links import Links
    from flask_app.app.resources.ratings import Ratings
    from flask_app.app.resources.tags import Tags

    api.add_resource(HelloWorld, "/")
    api.add_resource(Movies, "/movies")
    api.add_resource(Links, "/links")
    api.add_resource(Ratings, "/ratings")
    api.add_resource(Tags, "/tags")

    return app
