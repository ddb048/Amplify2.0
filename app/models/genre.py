# from .user import User
from sqlalchemy import ForeignKey

from .db import SCHEMA, add_prefix_for_prod, db, environment


class Genre(db.Model):
    __tablename__ = 'genres'
    if environment == "production":
        __table_args__ = {'schema': SCHEMA}
    id = db.Column(db.Integer, primary_key = True)
    genre = db.Column(db.String, nullable = False)
 #relationship
    tracks = db.relationship('Track', back_populates = 'genres', cascade='all, delete')
    artists = db.relationship('Artist', back_populates = 'genres', cascade='all, delete')
    albums = db.relationship('Album', back_populates = 'genres', cascade='all, delete')

    def to_dict(self):
        return {
            'id': self.id,
            'genre': self.genre
        }
