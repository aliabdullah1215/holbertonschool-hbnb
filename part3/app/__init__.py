from flask import Flask
from flask_restx import Api
from flask_cors import CORS  # التعديل 1: استيراد مكتبة CORS
from .extensions import db, bcrypt, jwt  # استيراد من الملف الجديد
from config import config

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    
    # تفعيل CORS للسماح لطلبات Part 4 (الواجهة الأمامية) بالوصول للـ API
    # التعديل 2: تفعيل CORS
    CORS(app)

    # التحقق مما إذا كان المدخل نصاً للمسار أو اسماً للبيئة
    if isinstance(config_class, str):
        if config_class.startswith("config."):
            app.config.from_object(config_class)
        else:
            app.config.from_object(config.get(config_class, config['default']))
    else:
        app.config.from_object(config_class)

    # 1. تهيئة الإضافات الأساسية من extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # 2. تعريف كائن الـ API المركزي
    api = Api(app, 
              version='1.0', 
              title='HBnB API', 
              description='HBnB Application API with Authentication',
              doc='/api/v1/')

    # 3. استيراد الـ Namespaces داخل سياق التطبيق لكسر دائرة الاستيراد
    with app.app_context():
        from app.api.v1.users import api as users_ns
        from app.api.v1.auth import api as auth_ns
        from app.api.v1.amenities import api as amenities_ns
        from app.api.v1.places import api as places_ns
        from app.api.v1.reviews import api as reviews_ns

        # 4. تسجيل الـ Namespaces
        api.add_namespace(users_ns, path='/api/v1/users')
        api.add_namespace(auth_ns, path='/api/v1/auth')
        api.add_namespace(amenities_ns, path='/api/v1/amenities')
        api.add_namespace(places_ns, path='/api/v1/places')
        api.add_namespace(reviews_ns, path='/api/v1/reviews')
        
    return app
