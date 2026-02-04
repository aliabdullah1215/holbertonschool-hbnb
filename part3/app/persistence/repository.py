from app import db

class Repository:
    """Abstract repository interface defining CRUD operations."""

    def add(self, obj):
        raise NotImplementedError

    def get(self, obj_id):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def update(self, obj_id, data):
        raise NotImplementedError

    def delete(self, obj_id):
        raise NotImplementedError

    def get_by_attribute(self, attr_name, attr_value):
        raise NotImplementedError


class SQLAlchemyRepository(Repository):
    """SQLAlchemy-based repository implementation."""

    def __init__(self, model):
        """Initialize with a SQLAlchemy model."""
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None
        
        # التعديل الجوهري هنا:
        # إذا كانت data قاموساً (تحديث عادي)
        if isinstance(data, dict):
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
        # إذا كانت data هي الكائن نفسه (تحديث علاقات مثل Amenities)
        # التغييرات تمت بالفعل في الـ Facade، نحتاج فقط للـ commit
        
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
            
        return obj

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            return None
        db.session.delete(obj)
        db.session.commit()
        return obj

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
