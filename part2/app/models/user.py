#!/usr/bin/python3
"""User model"""

from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email):
        super().__init__()

        if not first_name or not isinstance(first_name, str):
            raise ValueError("first_name must be a non-empty string")
        if not last_name or not isinstance(last_name, str):
            raise ValueError("last_name must be a non-empty string")
        if not email or not isinstance(email, str):
            raise ValueError("email must be a non-empty string")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email

