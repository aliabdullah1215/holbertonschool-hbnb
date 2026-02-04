#!/usr/bin/python3
"""Place model"""

from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship

# تعريف الجدول الوسيط هنا قبل كلاس Place لمنع الاستيراد الدائري
place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, default=0.0)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # تغيير النوع إلى String(36) ليتوافق مع UUID الخاص بجدول المستخدمين
    owner_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

# في ملف place.py
    reviews = relationship(
        "Review",
        back_populates="place",  # الربط المتبادل بالاسم
        lazy="select",
        cascade="all, delete-orphan"
    )

    # نستخدم اسم الكلاس كنص "Amenity"
    amenities = relationship(
        "Amenity",
        secondary=place_amenity,
        backref="places",  # استخدمنا backref لسهولة الربط من الطرفين
        lazy="subquery"
    )

    def __init__(self, **kwargs):
        """Initialize Place"""
        # نمرر الكلمات المفتاحية للـ super() ليتعامل معها BaseModel و SQLAlchemy
        super().__init__(**kwargs)

    def add_review(self, review):
        from app.models.review import Review
        if not isinstance(review, Review):
            raise ValueError("review must be a Review instance")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        from app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")
        self.amenities.append(amenity)
