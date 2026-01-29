#!/usr/bin/python3
"""Review model"""

from app import db
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place
from sqlalchemy.orm import relationship

class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.Integer, db.ForeignKey("places.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    place = relationship("Place", backref="reviews")
    user = relationship("User", backref="reviews")

    def __init__(self, place, user, text, rating):
        super().__init__()

        if not isinstance(place, Place):
            raise ValueError("place must be a Place instance")
        if not isinstance(user, User):
            raise ValueError("user must be a User instance")
        if not text or not isinstance(text, str):
            raise ValueError("text must be a non-empty string")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("rating must be an integer between 1 and 5")

        self.place = place
        self.user = user
        self.text = text
        self.rating = rating
