#!/usr/bin/python3
"""Place model"""

from app import db
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity
from sqlalchemy.orm import relationship

place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.Integer, db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.Integer, db.ForeignKey("amenities.id"), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, default=0.0)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    reviews = relationship(
        "Review",
        backref="place",
        lazy="select",
        cascade="all, delete-orphan"
    )

    amenities = relationship(
        "Amenity",
        secondary=place_amenity,
        back_populates="places",
        lazy="subquery"
    )

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

        if not title or not isinstance(title, str):
            raise ValueError("title must be a non-empty string")
        if len(title) > 100:
            raise ValueError("title must be at most 100 characters")

        if not isinstance(owner, User):
            raise ValueError("owner must be a User instance")

        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("price must be a number >= 0")

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

        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        from app.models.review import Review
        if not isinstance(review, Review):
            raise ValueError("review must be a Review instance")
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")
        self.amenities.append(amenity)
        self.save()
