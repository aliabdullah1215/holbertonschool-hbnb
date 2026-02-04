from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api

# تعريف الكائنات الأساسية في النطاق العام
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. تهيئة الإضافات الأساسية
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # 2. تعريف كائن الـ API المركزي
    # ملاحظة: جعلنا الـ doc يفتح على الجذر لمشاهدة التوثيق بسهولة
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
        from app.api.v1.reviews import api as reviews_ns # تم تغيير الاسم هنا للاتساق

        # 4. تسجيل الـ Namespaces
        # قمت بتوحيد نمط المسارات لضمان عمل الـ Review
        api.add_namespace(users_ns, path='/api/v1/users')
        api.add_namespace(auth_ns, path='/api/v1/auth')
        api.add_namespace(amenities_ns, path='/api/v1/amenities')
        api.add_namespace(places_ns, path='/api/v1/places')
        api.add_namespace(reviews_ns, path='/api/v1/reviews') # التعديل هنا ليعمل طلبك
        
    return app
