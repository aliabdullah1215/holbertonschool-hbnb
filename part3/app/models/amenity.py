#!/usr/bin/python3
"""Amenity model"""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Represents an amenity (e.g., Wi-Fi, Pool)"""

    def __init__(self, name):
        super().__init__()

        if not name or not isinstance(name, str):
            raise ValueError("name must be a non-empty string")
        if len(name) > 50:
            raise ValueError("name must be at most 50 characters")

        self.name = name

