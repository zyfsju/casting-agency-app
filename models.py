# from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os
from datetime import datetime


database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
database_path = os.environ.get("DATABASE_URL", database_path)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    """
        Binds a flask application and a SQLAlchemy service
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


# class Base(db.Model):
#     def insert(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()


class Movie(db.Model):
    """
        Movies with attributes title and release date
    """

    __tablename__ = "Movie"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    # actors = db.relationship(
    #     "Actor", secondary=movie_actors, backref=db.backref("movies", lazy=True)
    # )

    def format(self):
        if isinstance(self.release_date, datetime):
            release_date = self.release_date.strftime("%Y-%m-%d")
        else:
            release_date = self.release_date
        return {"id": self.id, "title": self.title, "release_date": release_date}

    def insert(self):
        if self.release_date and not isinstance(self.release_date, datetime):
            self.release_date = datetime.strptime(self.release_date, "%Y-%m-%d")
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        if self.release_date and not isinstance(self.release_date, datetime):
            self.release_date = datetime.strptime(self.release_date, "%Y-%m-%d")
        db.session.commit()


class Actor(db.Model):
    """
        Actors with attributes name, age and gender
    """

    __tablename__ = "Actor"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


movie_actors = db.Table(
    "movie_actors",
    db.Column("movie_id", db.Integer, db.ForeignKey("Movie.id"), primary_key=True),
    db.Column("actor_id", db.Integer, db.ForeignKey("Actor.id"), primary_key=True),
)


class Relation(db.Model):
    __tablename__ = "Relation"

    movie_id = db.Column(
        "movie_id", db.Integer, db.ForeignKey("Movie.id"), primary_key=True
    )
    actor_id = db.Column(
        "actor_id", db.Integer, db.ForeignKey("Actor.id"), primary_key=True
    )
    movies = db.relationship(
        "Movie", foreign_keys="Relation.movie_id", backref="relation"
    )
    actors = db.relationship(
        "Actor", foreign_keys="Relation.actor_id", backref="relation"
    )
