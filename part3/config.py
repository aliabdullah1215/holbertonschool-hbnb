import os

# تحديد المجلد الرئيسي للمشروع للحصول على مسار مطلق لقاعدة البيانات
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    # إضافة مسار قاعدة البيانات هنا
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'development.db')
