import unittest
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        """إعداد البيئة وتجهيز البيانات المطلوبة للاختبارات"""
        self.app = create_app()
        self.client = self.app.test_client()

        # 1. إنشاء مستخدم ليكون صاحب المكان (Owner)
        user_res = self.client.post('/api/v1/users/', json={
            "first_name": "John", 
            "last_name": "Doe", 
            "email": "john.place@example.com"
        })
        
        user_data = user_res.get_json()
        if 'id' not in user_data:
            print(f"User creation failed: {user_data}")
            
        self.owner_id = user_data['id']

        # 2. إنشاء مرفق (Amenity)
        amenity_res = self.client.post('/api/v1/amenities/', json={"name": "WiFi"})
        self.amenity_id = amenity_res.get_json()['id']

    def test_create_place_success(self):
        """اختبار إنشاء مكان بنجاح مع ربطه بالمالك والمرافق"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Luxury Apartment",
            "description": "A beautiful place to stay",
            "price": 150.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.owner_id,
            "amenities": [self.amenity_id]
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['title'], "Luxury Apartment")
        self.assertEqual(len(data['amenities']), 1)

    def test_create_place_invalid_price(self):
        """اختبار منع إنشاء مكان بسعر سالب (Validation Check)"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Cheap Room",
            "price": -10.0,
            "latitude": 0, 
            "longitude": 0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Price must be a number >= 0", response.get_json()['error'])

    def test_get_all_places(self):
        """اختبار جلب قائمة الأماكن"""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_place_not_found(self):
        """اختبار محاولة جلب مكان غير موجود"""
        response = self.client.get('/api/v1/places/invalid_id')
        self.assertEqual(response.status_code, 404)
