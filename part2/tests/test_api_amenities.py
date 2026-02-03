import unittest
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity_success(self):
        """Test successful amenity creation"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_create_amenity_invalid_data(self):
        """Test creation with invalid name (empty string)"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_get_amenities_list(self):
        """Test retrieving the list of amenities"""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_amenity_by_id(self):
        """Test retrieving a specific amenity by ID"""
        create_res = self.client.post('/api/v1/amenities/', json={
            "name": "Pool"
        })
        amenity_id = create_res.get_json()['id']
        
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], "Pool")

    def test_get_amenity_not_found(self):
        """Test retrieving a non-existent amenity"""
        response = self.client.get('/api/v1/amenities/invalid-id')
        self.assertEqual(response.status_code, 404)
