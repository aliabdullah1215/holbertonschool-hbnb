#!/usr/bin/python3
"""Place model"""

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


class Place(BaseModel):
    """Represents a place (house, apartment, room, etc.)"""

    def __init__(self, title, owner, description="", price=0.0, latitude=None, longitude=None):
        super().__init__()
        self.title = title
        self.owner = owner
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Title must be a non-empty string")
        if len(value) > 100:
            raise ValueError("Title must be at most 100 characters")
        self._title = value

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise ValueError("Owner must be a User instance")
        self._owner = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a number >= 0")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if value is not None:
            if not isinstance(value, (int, float)) or not (-90 <= value <= 90):
                raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if value is not None:
            if not isinstance(value, (int, float)) or not (-180 <= value <= 180):
                raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value

    def add_review(self, review):
        """Add a review to this place"""
        from app.models.review import Review
        if not isinstance(review, Review):
            raise ValueError("Review must be a Review instance")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to this place"""
        if not isinstance(amenity, Amenity):
            raise ValueError("Amenity must be an Amenity instance")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
