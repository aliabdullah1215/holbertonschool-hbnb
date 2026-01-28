#!/usr/bin/python3
"""User model"""

import re
from app import db, bcrypt
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates


class User(BaseModel):
    """Represents a user in HBnB"""

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # -------- Validators --------
    @validates('first_name')
    def validate_first_name(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("first_name must be a non-empty string")
        if len(value) > 50:
            raise ValueError("first_name must be at most 50 characters")
        return value

    @validates('last_name')
    def validate_last_name(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("last_name must be a non-empty string")
        if len(value) > 50:
            raise ValueError("last_name must be at most 50 characters")
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("email must be a non-empty string")

        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_pattern, value):
            raise ValueError("email must be a valid email address")

        return value.lower()

    # -------- Password methods --------
    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
