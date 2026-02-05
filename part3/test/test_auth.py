import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app('config.TestingConfig') # نسخة خاصة للاختبار
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_login_success(client):
    # نرسل طلب تسجيل دخول وهمي
    response = client.post('/api/v1/auth/login', json={
        "email": "admin@hbnb.io",
        "password": "admin1234"
    })
    assert response.status_code == 200
    assert "access_token" in response.get_json()
