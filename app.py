#!/usr/bin/env python3
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import Actor, Movie, setup_db
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
    return app


APP = create_app()

"""
Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies
and managing and assigning actors to those movies. You are an Executive
Producer within the company and are creating a system to simplify and
streamline your process.

Models:

Movies with attributes title and release date
Actors with attributes name, age and gender

Endpoints:
GET /actors and /movies
DELETE /actors/ and /movies/
POST /actors and /movies and
PATCH /actors/ and /movies/

Roles:
Casting Assistant
    Can view actors and movies
Casting Director
    All permissions a Casting Assistant has and…
    Add or delete an actor from the database
    Modify actors or movies
Executive Producer
    All permissions a Casting Director has and…
    Add or delete a movie from the database

Tests:
One test for success behavior of each endpoint
One test for error behavior of each endpoint
At least two tests of RBAC for each role
"""


@APP.route("/actors")
@requires_auth("get:actors")
def get_actors():
    try:
        actors = [x.format() for x in Actor.query.all()]
    except AuthError as e:
        abort(e)
    except:
        abort(422)
    return jsonify(success=True, actors=actors)


@APP.route("/movies")
@requires_auth("get:movies")
def get_movies():
    try:
        movies = [x.format() for x in Movie.query.all()]
    except AuthError as e:
        abort(e)
    except:
        abort(422)
    return jsonify(success=True, movies=movies)


@APP.route("/actors", methods=["POST"])
@requires_auth("post:actors")
def add_new_actor():
    try:
        actor = request.get_json()
        actor = Actor(**{k: actor.get(k) for k in ["name", "age", "gender"]})
        actor.insert()
    except AuthError as e:
        abort(e)
    except:
        abort(422)
    return jsonify(success=True, actors=[actor.format()])


@APP.route("/movies", methods=["POST"])
@requires_auth("post:movies")
def add_new_movie():
    try:
        movie = request.get_json()
        movie = Movie(title=movie.get("title"), release_date=movie.get("release_date"))
        movie.insert()
    except AuthError as e:
        abort(e)
    except:
        abort(422)
    return jsonify(success=True, movies=[movie.format()])


@APP.route("/actors/<int:actor_id>", methods=["PATCH"])
@requires_auth("patch:actors")
def update_actor(actor_id):
    new_actor = request.get_json()
    actor = Drink.query.get(actor_id)
    if not actor:
        abort(404)
    try:
        for k, v in new_actor.items():
            setattr(actor, k, v)
        actor.update()
    except Exception as e:
        abort(422)
    return jsonify(success=True, actors=[actor.format()])


@APP.route("/movies/<int:movie_id>", methods=["PATCH"])
@requires_auth("patch:movies")
def update_movie(movie_id):
    new_movie = request.get_json()
    movie = Drink.query.get(movie_id)
    if not movie:
        abort(404)
    try:
        for k, v in new_movie.items():
            setattr(movie, k, v)
        movie.update()
    except Exception as e:
        abort(422)
    return jsonify(success=True, movies=[movie.format()])


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": 404, "message": "Not found"}), 404


@app.errorhandler(AuthError)
def auth_error(error):
    return (
        jsonify(
            {
                "success": False,
                "error": error.status_code,
                # "message": error.error.get("description"),
                **error.error,
            }
        ),
        error.status_code,
    )


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=8080, debug=True)
