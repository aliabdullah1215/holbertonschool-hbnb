#!/usr/bin/python3
"""Place model"""

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


class Place(BaseModel):
    """Represents a place (house, apartment, room, etc.)"""

    def __init__(
        self,
        title,
        owner,
        description="",
        price=0.0,
        latitude=None,
        longitude=None
    ):
        super().__init__()

        # Validate title
        if not title or not isinstance(title, str):
            raise ValueError("title must be a non-empty string")
        if len(title) > 100:
            raise ValueError("title must be at most 100 characters")

        # Validate owner (must be User instance)
        if not isinstance(owner, User):
            raise ValueError("owner must be a User instance")

        # Validate price
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("price must be a number >= 0")

        # Validate latitude / longitude if provided
        if latitude is not None:
            if not isinstance(latitude, (int, float)) or not (-90 <= latitude <= 90):
                raise ValueError("latitude must be between -90 and 90")
        if longitude is not None:
            if not isinstance(longitude, (int, float)) or not (-180 <= longitude <= 180):
                raise ValueError("longitude must be between -180 and 180")

        self.title = title
        self.owner = owner
        self.description = description
        self.price = float(price)
        self.latitude = latitude
        self.longitude = longitude

        # Relationships
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review to this place"""
        from app.models.review import Review  # local import to avoid circular import

        if not isinstance(review, Review):
            raise ValueError("review must be a Review instance")
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        """Add an amenity to this place"""
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")
        self.amenities.append(amenity)
        self.save()

