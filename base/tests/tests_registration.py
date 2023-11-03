from rest_framework.test import APITestCase
from base.models import user

class RegistrationTest(APITestCase):
    def setUp(self):
        self.data = {
            "username": "success",
            "password": "success"
        }
        
    def test_registration_success(self):
        
        response = self.client.post('/register/', self.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'username': 'success', 'password': 'success'})
        self.assertTrue(user.objects.filter(username='success').exists())
        
    def test_registration_failure(self):
        
        user.objects.create(username = "success", password = "success")
        response = self.client.post('/register/', self.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'username': ['user with this username already exists.']})