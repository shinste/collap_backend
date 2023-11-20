from rest_framework.test import APITestCase
from base.models import user
from .common_methods import checker

# Test class that unit tests the registration endpoint
# Testing:
# registration success (status, response, model), registration failure (status, response)
class RegistrationTest(APITestCase):
    def setUp(self):
        self.data = {
            "username": "success",
            "password": "success"
        }
        
    def test_registration_success(self):
        response = self.client.post('/register/', self.data)
        # special status code 201
        checker(self, response, {'username': 'success', 'password': 'success'}, 201)
        self.assertTrue(user.objects.filter(username='success').exists())
        
    def test_registration_name_failure(self):
        user.objects.create(username = "success", password = "success")
        
        response = self.client.post('/register/', self.data)
        checker(self, response, {'username': ['user with this username already exists.']}, 400)
        
    def test_registration_input_failure(self):
        response = self.client.post('/register/', {})
        checker(self, response, {'password': ['This field is required.'],
                                 'username': ['This field is required.']}, 400)