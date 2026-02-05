from app.extensions import db  # التغيير هنا لاستخدام ملف الامتدادات
from sqlalchemy.exc import SQLAlchemyError

class Repository:
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
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database Add Error: {e}")
            raise e

    def get(self, obj_id):
        # تم التحديث هنا لإزالة تحذير LegacyAPIWarning
        # الطريقة الحديثة في SQLAlchemy 2.0
        return db.session.get(self.model, obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None
        try:
            if isinstance(data, dict):
                for key, value in data.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
            db.session.commit()
            return obj
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database Update Error: {e}")
            raise e

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            return None
        try:
            db.session.delete(obj)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database Delete Error: {e}")
            raise e

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
