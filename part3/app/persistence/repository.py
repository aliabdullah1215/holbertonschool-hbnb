from app import db


class SQLAlchemyRepository(Repository):
    """SQLAlchemy-based repository implementation."""

    def __init__(self, model):
        self.model = model

    def add(self, entity):
        db.session.add(entity)
        db.session.commit()
        return entity

    def get(self, entity_id):
        return self.model.query.get(entity_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, entity_id, data):
        entity = self.get(entity_id)
        if not entity:
            return None
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        db.session.commit()
        return entity

    def delete(self, entity_id):
        entity = self.get(entity_id)
        if not entity:
            return None
        db.session.delete(entity)
        db.session.commit()
        return entity

    def get_by_attribute(self, attribute, value):
        return self.model.query.filter_by(**{attribute: value}).first()
