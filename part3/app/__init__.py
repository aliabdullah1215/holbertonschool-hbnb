import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture
def client():
    # تمرير المسار النصي الكامل كما يتوقعه ملف __init__.py لديك
    app = create_app('config.TestingConfig') 
    
    with app.test_client() as client:
        with app.app_context():
            # إنشاء الجداول في قاعدة بيانات الذاكرة
            db.create_all()

            # زرع بيانات المستخدم المسؤول (Admin)
            if not User.query.filter_by(email="admin@hbnb.io").first():
                admin_user = User(
                    email="admin@hbnb.io",
                    first_name="Admin",
                    last_name="HBnB",
                    is_admin=True
                )
                admin_user.hash_password("admin1234")
                db.session.add(admin_user)
                db.session.commit()

            yield client

            # التنظيف بعد الاختبار
            db.session.remove()
            db.drop_all()

def test_login_success(client):
    """اختبار تسجيل الدخول بنجاح والتحقق من التوكن"""
    response = client.post('/api/v1/auth/login', json={
        "email": "admin@hbnb.io",
        "password": "admin1234"
    })
    
    # في حال الفشل، اطبع الرد للمساعدة في التشخيص
    if response.status_code != 200:
        print(f"\nResponse Body: {response.get_json()}")

    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
