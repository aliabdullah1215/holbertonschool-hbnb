from abc import ABC, abstractmethod


class Repository(ABC):
    """Abstract base class for repositories."""

    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def get(self, entity_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, entity_id, data):
        pass

    @abstractmethod
    def delete(self, entity_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attribute, value):
        pass


class InMemoryRepository(Repository):
    """Simple in-memory repository using a dictionary."""

    def __init__(self):
        self.storage = {}

    def add(self, entity):
        self.storage[str(entity.id)] = entity
        return entity

    def get(self, entity_id):
        return self.storage.get(str(entity_id))

    def get_all(self):
        return list(self.storage.values())

    def update(self, entity_id, data):
        entity = self.get(entity_id)
        if not entity:
            return None
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        if hasattr(entity, "save") and callable(getattr(entity, "save")):
            entity.save()
        return entity

    def delete(self, entity_id):
        return self.storage.pop(str(entity_id), None)

    def get_by_attribute(self, attribute, value):
        for entity in self.storage.values():
            if getattr(entity, attribute, None) == value:
                return entity
        return None

