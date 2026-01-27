#!/usr/bin/python3
"""Base model for all HBnB entities"""

import uuid
from datetime import datetime


class BaseModel:
    """BaseModel defines common attributes and methods"""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def save(self):
        """
        Update the updated_at timestamp
        """
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """
        Update attributes from a dictionary and save changes
        """
        if not isinstance(data, dict):
            raise TypeError("update() expects a dictionary")

        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.save()

