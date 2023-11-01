from django.test import TestCase, RequestFactory
from rest_framework.test import APITestCase
from base.models import *
from django.http import HttpRequest
from ..views import *
import json
import requests

class RegistrationTest(APITestCase):
    def setUp(self):
        self.data = {
            "username": "success",
            "password": "success"
        }
    def test_registration_success(self):
        
        response = self.client.post('/register/', self.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertTrue(user.objects.filter(username='success').exists())
        
    def test_registration_failure(self):
        user.objects.create(username = "success", password = "success")
        response = self.client.post('/register/', self.data)
        self.assertEqual(response.status_code, 400)

# create event test first
class NotificationTest(TestCase):
    def setUp(self):
        self.user = user.objects.create(username = "notification", password = "success")
        self.event = {
            "event_id": "testevent",
            "name": "testname",
            "primary_date": "2023-03-23",
            "host": "notification"
        }
        event_instance = Event.objects.create(event_id= "testevent",
                                              name= "testname",
                                              primary_date= "2023-03-23",
                                              host= self.user)
        self.notification = {
            "id": 8,
            "event_id_id": "testing",
            "username_id": "test",
            "notification": "testing notif"
        }
        self.factory = RequestFactory()
        Notification.objects.create(id = 439854,
                                    event_id = event_instance,
                                    username = self.user,
                                    notification = "testing notif")
    def test_notification_empty(self):
        
        response = self.client.get('/notification/', {"username": "success"})
        self.assertEqual(response.status_code, 400)
    def test_notification_full(self):
        request = self.factory.get("/notification/")
        request.user = self.user
        response = notification_view(request)
        
        
        # testrequest = HttpRequest()
        # testrequest.method = 'GET'
        # testrequest.GET['username'] = 'notification'
        # testrequest.content_type = 'application/json'
        # testrequest._read_started = False
        
        # response = notification_view(testrequest)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.objects.filter(username='notification').exists())
        sdfsdfds