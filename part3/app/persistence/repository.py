# app/persistence/repository.py

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
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception as e:
            db.session.rollback()
            raise e

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        """
        تحديث الكائن. 
        إذا كان data قاموساً، يتم تحديث الحقول. 
        إذا كان data هو الكائن نفسه (معدل مسبقاً في Facade)، يتم عمل commit فقط.
        """
        obj = self.get(obj_id)
        if not obj:
            return None
        
        try:
            # إذا أرسلنا قاموساً (تحديث حقول نصية مثلاً)
            if isinstance(data, dict):
                for key, value in data.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
            
            # إذا أرسلنا الكائن نفسه، فالقيم تم تغييرها في الـ Facade 
            # ولا نحتاج لعمل setattr، الـ SQLAlchemy سيكتشف التغييرات تلقائياً
            
            db.session.commit()
            return obj
        except Exception as e:
            db.session.rollback()
            # لضمان معرفة سبب الخطأ في نافذة السيرفر
            print(f"Update Error: {e}")
            raise e

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            return None
        try:
            db.session.delete(obj)
            db.session.commit()
            return obj
        except Exception as e:
            db.session.rollback()
            raise e

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
