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

    def save(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def update(self, data):
        """Update attributes from a dictionary and save changes"""
        if not isinstance(data, dict):
            raise TypeError("update() expects a dictionary")

        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.save()
