#!/usr/bin/python3
"""Base model for all HBnB entities"""

import uuid
from datetime import datetime
from app import db


class BaseModel(db.Model):
    """Abstract BaseModel mapped with SQLAlchemy"""

    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def __init__(self, **kwargs):
        """Initialize the model with attributes from kwargs"""
        super().__init__()
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # التأكد من وجود ID في حال لم يتم توفيره
        if not self.id:
            self.id = str(uuid.uuid4())

    def save(self):
        """Save the object to the database and update timestamp"""
        self.updated_at = datetime.utcnow()
        db.session.add(self)  # تأكيد إضافة الكائن للجلسة
        db.session.commit()

    def delete(self):
        """Delete the object from the database"""
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        """Update attributes from a dictionary and save changes"""
        if not isinstance(data, dict):
            raise TypeError("update() expects a dictionary")

        for key, value in data.items():
            # نتجنب تحديث الحقول الأساسية يدوياً لضمان سلامة البيانات
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)

        self.save()
