import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture
def client():
    # التعديل الجوهري: تمرير المسار النصي الكامل كما يتوقعه ملف __init__.py لديك
    # هذا المسار يخبر Flask: اذهب لملف config.py وابحث عن كلاس TestingConfig
    app = create_app('config.TestingConfig') 
    
    with app.test_client() as client:
        with app.app_context():
            # إنشاء الجداول في قاعدة بيانات الذاكرة (:memory:)
            db.create_all()

            # إنشاء مستخدم مسؤول (Admin) يدويًا لأن قاعدة بيانات الاختبار تبدأ فارغة
            admin_user = User(
                email="admin@hbnb.io",
                first_name="Admin",
                last_name="HBnB",
                is_admin=True
            )
            # تشفير كلمة المرور (تأكد أن الموديل يحتوي على هذه الدالة)
            admin_user.hash_password("admin1234")
            
            db.session.add(admin_user)
            db.session.commit()

            yield client

            # تنظيف قاعدة البيانات بعد الانتهاء
            db.session.remove()
            db.drop_all()

def test_login_success(client):
    """اختبار تسجيل الدخول بنجاح للمستخدم المسؤول والتحقق من التوكن"""
    response = client.post('/api/v1/auth/login', json={
        "email": "admin@hbnb.io",
        "password": "admin1234"
    })
    
    # في حال فشل الاختبار، سيطبع التيرمنال رد السيرفر للمساعدة في التشخيص
    if response.status_code != 200:
        print(f"\nخطأ في الرد: {response.get_json()}")

    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
