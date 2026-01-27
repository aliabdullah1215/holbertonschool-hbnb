#!/usr/bin/python3
"""User model"""

import re
from app.models.base_model import BaseModel


class User(BaseModel):
    """Represents a user in HBnB"""

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        # Validate first_name
        if not first_name or not isinstance(first_name, str):
            raise ValueError("first_name must be a non-empty string")
        if len(first_name) > 50:
            raise ValueError("first_name must be at most 50 characters")

        # Validate last_name
        if not last_name or not isinstance(last_name, str):
            raise ValueError("last_name must be a non-empty string")
        if len(last_name) > 50:
            raise ValueError("last_name must be at most 50 characters")

        # Validate email
        if not email or not isinstance(email, str):
            raise ValueError("email must be a non-empty string")

        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_pattern, email):
            raise ValueError("email must be a valid email address")

        # Validate is_admin
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

