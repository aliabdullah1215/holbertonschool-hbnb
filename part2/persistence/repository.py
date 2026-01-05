#!/usr/bin/env python3
"""
Repository interface for HBnB project.
Defines the common methods for any persistence mechanism.
"""

from abc import ABC, abstractmethod


class Repository(ABC):
    """Abstract base class for repositories"""

    @abstractmethod
    def add(self, obj):
        """Add a new object to the repository"""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by its ID"""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieve all objects"""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an existing object"""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object by its ID"""
        pass
