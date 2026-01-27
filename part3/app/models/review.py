#!/usr/bin/python3
"""Review model"""

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    """Represents a review made by a user on a place"""

    def __init__(self, place, user, text, rating):
        super().__init__()

        # Validate place and user are instances
        if not isinstance(place, Place):
            raise ValueError("place must be a Place instance")
        if not isinstance(user, User):
            raise ValueError("user must be a User instance")

        # Validate text
        if not text or not isinstance(text, str):
            raise ValueError("text must be a non-empty string")

        # Validate rating
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("rating must be an integer between 1 and 5")

        self.place = place
        self.user = user
        self.text = text
        self.rating = rating

