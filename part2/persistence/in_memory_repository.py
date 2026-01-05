#!/usr/bin/env python3
"""
In-memory repository implementation for HBnB project.
Stores objects in memory using a dictionary.
"""

from persistence.repository import Repository


class InMemoryRepository(Repository):
    """In-memory implementation of the Repository interface"""

    def __init__(self):
        """Initialize the in-memory storage"""
        self._storage = {}

    def add(self, obj):
        """
        Add a new object to the repository.
        The object must have an 'id' attribute.
        """
        self._storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        """Retrieve an object by its ID"""
        return self._storage.get(obj_id)

    def get_all(self):
        """Retrieve all objects"""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Update an existing object with provided data.
        'data' is a dictionary of attributes to update.
        """
        obj = self.get(obj_id)
        if not obj:
            return None

        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        return obj

    def delete(self, obj_id):
        """Delete an object by its ID"""
        return self._storage.pop(obj_id, None)
