# from .user import User
from sqlalchemy import ForeignKey

from .db import SCHEMA, add_prefix_for_prod, db, environment


class Artist(db.Model):
    __tablename__ = 'artists'
    if environment == "production":
        __table_args__ = {'schema': SCHEMA}
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    genre_id = db.Column(db.Integer, ForeignKey(add_prefix_for_prod("genres.id")))
    artist_pic = db.Column(db.String(255))
    description = db.Column(db.String(255))
 #relationship
    genres = db.relationship('Genre', back_populates = 'artists')
    albums = db.relationship('Album', back_populates = 'artists', cascade='all, delete')
    tracks = db.relationship('Track', back_populates = 'artists', cascade='all, delete')
    follows = db.relationship('Follow', back_populates = 'artists', cascade = 'all, delete')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'artist_pic': self.artist_pic,
            'description': self.description,
            'genre': self.genres.to_dict(),
            'follows': [follow.to_dict() for follow in self.follows]
        }
