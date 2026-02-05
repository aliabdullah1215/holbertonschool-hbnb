import pytest
from app import create_app
from app.extensions import db
from app.models.user import User

@pytest.fixture
def client():
    # استخدام إعدادات الاختبار
    app = create_app('config.TestingConfig') 
    
    with app.test_client() as client:
        with app.app_context():
            # إنشاء الجداول في قاعدة بيانات الذاكرة (:memory:)
            db.create_all()

            # إنشاء مستخدم مسؤول (Admin) للاختبار
            admin_user = User(
                email="admin@hbnb.io",
                first_name="Admin",
                last_name="HBnB",
                is_admin=True
            )
            # تشفير كلمة المرور
            admin_user.hash_password("admin1234")
            
            db.session.add(admin_user)
            db.session.commit()

            yield client

            # تنظيف بعد الانتهاء
            db.session.remove()
            db.drop_all()

def test_login_success(client):
    """اختبار تسجيل الدخول الناجح للمستخدم المسؤول"""
    response = client.post('/api/v1/auth/login', json={
        "email": "admin@hbnb.io",
        "password": "admin1234"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data

def test_login_wrong_password(client):
    """اختبار رفض تسجيل الدخول عند استخدام كلمة مرور خاطئة"""
    response = client.post('/api/v1/auth/login', json={
        "email": "admin@hbnb.io",
        "password": "wrongpassword"
    })
    # الـ API يرجع 401 عند الخطأ
    assert response.status_code == 401
    # التعديل هنا ليطابق رد الـ API الخاص بك
    data = response.get_json()
    assert data.get("error") == "Invalid email or password"

def test_login_invalid_user(client):
    """اختبار رفض تسجيل الدخول لمستخدم غير موجود في القاعدة"""
    response = client.post('/api/v1/auth/login', json={
        "email": "nonexistent@hbnb.io",
        "password": "password123"
    })
    assert response.status_code == 401
    assert "error" in response.get_json()
