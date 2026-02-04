#!/usr/bin/python3
"""Review model"""

from app import db
from app.models.base_model import BaseModel

class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # معرفات العلاقات (UUIDs)
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    # العلاقات مع الجداول الأخرى
    place = db.relationship("Place", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")

    def __init__(self, **kwargs):
        """
        Initialize Review with validation
        """
        # التحقق من صحة التقييم قبل الإنشاء
        rating = kwargs.get('rating')
        if rating is not None:
            try:
                rating = int(rating)
                if not (1 <= rating <= 5):
                    raise ValueError("Rating must be between 1 and 5")
                kwargs['rating'] = rating
            except (ValueError, TypeError):
                raise ValueError("Rating must be an integer between 1 and 5")

        # التحقق من وجود النص
        text = kwargs.get('text')
        if text is not None:
            if not isinstance(text, str) or len(text.strip()) == 0:
                raise ValueError("Text must be a non-empty string")

        super().__init__(**kwargs)
