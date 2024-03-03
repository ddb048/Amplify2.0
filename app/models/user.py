from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .db import SCHEMA, add_prefix_for_prod, db, environment
from .follow import Follow
from .like import Like

# Imports SQL Alchemy db object for ORM operations
# environment is used to determine if the app is in production or development
# SCHEMA is used to determine the schema of the database
# add_prefix_for_prod is used to add a prefix to the table name if the app is in production


# imports the generate_password_hash and check_password_hash functions from werkzeug.security
# these functions are used to hash and check hashed passwords


# imports the UserMixin class from flask_login
# UserMixin is used to add default implementations of methods required by the Flask-Login extension


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    playlists = db.relationship('Playlist', back_populates='users', cascade="all,delete")
    follows = db.relationship('Follow', back_populates='users', cascade="all,delete")
    likes = db.relationship('Like', back_populates='users', cascade="all,delete")
    queue = db.relationship('Queue', back_populates='users')

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def like_track(self, track):
        if not self.has_liked_track(track):
            like = Like(user_id=self.id, track_id=track.id)
            db.session.add(like)
        else:
            return {
            "errors": "Track already in your collection"
            }, 404

    def unlike_track(self, track):
        if self.has_liked_track(track):
            Like.query.filter_by(
                user_id=self.id,
                track_id=track.id).delete()
        else:
            return {
            "errors": "Track not currently in your collection"
            }, 404

    def has_liked_track(self, track):
        return Like.query.filter(
            Like.user_id == self.id,
            Like.track_id == track.id).count() > 0


    def follow_artist(self, artist):
        if not self.has_followed_artist(artist):
            follow = Follow(user_id=self.id, artist_id=artist.id)
            db.session.add(follow)
        else:
            return {
            "errors": "Artist already in your collection"
            }, 404

    def unfollow_artist(self, artist):
        if self.has_followed_artist(artist):
            Follow.query.filter_by(
                user_id=self.id,
                artist_id=artist.id).delete()
        else:
            return {
            "errors": "Artist not currently in your collection"
            }, 404

    def has_followed_artist(self, artist):
        return Follow.query.filter(
            Follow.user_id == self.id,
            Follow.artist_id == artist.id).count() > 0

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
