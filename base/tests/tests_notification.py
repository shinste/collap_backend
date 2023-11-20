from rest_framework.test import APITestCase
from base.models import Notification, user, Event
from .common_methods import checker

# Test class that unit tests the Notification endpoint
# Testing:
# notification success (status, response, model), registration failure (status, response)
class NotificationTest(APITestCase):
    def setUp(self):
        self.user = user.objects.create(username = "notification", password = "success")
        self.event = Event.objects.create(event_id= "testevent", name= "testname",
                                          primary_date= "2023-03-23", host= self.user)
        
    def test_notification_failure(self):
        response = self.client.get('/notification/', data={})
        checker(self, response,  {'error': 'Invalid JSON data'}, 400)
        
    def test_notification_success(self):
        Notification.objects.create(id = 439854, event_id = self.event,
                                    username = self.user,
                                    notification = "testing notif")

        response = self.client.get('/notification/', data={"username": "notification"})
        checker(self, response,  [{'event_id_id': 'testevent',
                                   'id': 439854,
                                   'notification': 'testing notif',
                                   'username_id': 'notification'}], 200)
        self.assertTrue(Notification.objects.filter(username='notification').exists())