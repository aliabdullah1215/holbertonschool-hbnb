#!/usr/bin/python3
"""Amenity model"""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Represents an amenity (e.g., Wi-Fi, Pool)"""

    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Amenity name must be a non-empty string")
        if len(value) > 50:
            raise ValueError("Amenity name must be at most 50 characters")
        self._name = value
