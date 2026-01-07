#!/usr/bin/env python3
"""
HBnB Facade
"""

from business_logic.user import User
from business_logic.amenity import Amenity
from persistence.in_memory_repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # =====================
    # User methods
    # =====================
    def create_user(self, **data):
        user = User(**data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def list_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, **data):
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(**data)
        return user

    # =====================
    # Amenity methods
    # =====================
    def create_amenity(self, name):
        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def list_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, name):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.update(name=name)
        return amenity


# Singleton Facade instance
facade = HBnBFacade()
