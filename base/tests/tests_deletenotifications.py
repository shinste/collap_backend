from rest_framework.test import APITestCase
from base.models import Notification, user, Event
from .common_methods import checker

# Test class that unit tests the Delete Notification endpoint
# Testing:
# delete notification success (status, response, model), delete notifications failure (status, response)
class DeleteNotifications(APITestCase):
    def setUp(self):
        host_instance = user.objects.create(username = "eventtestuser", password = "success")
        event_instance = Event.objects.create(event_id= "eventtest", name= "originaltest",
                                              primary_date= "2023-11-01", host= host_instance)
        participant1 = user.objects.create(username = "participant1", password = "success")
        Notification.objects.create(event_id = event_instance, username = participant1, notification = "testing notif")
    
    def test_delete_notification_input_failure(self):
        response = self.client.post('/delete_notifications/', data = {})
        checker(self, response, {'error':'Missing Input'}, 400)
        
    def test_delete_notification_input_failure(self):
        response = self.client.post('/delete_notifications/', data = {'event_id': "eventtest",
                                                                      'username': 'imaginaryfriend'})
        checker(self, response, {'error': "No notification found for this event/participant."}, 400)
    
    def test_delete_notification_success(self):
        response = self.client.post('/delete_notifications/', data = {'event_id' : "eventtest",
                                                                      'username' : 'participant1'})
        checker(self, response, {"status":"success"}, 200)
        self.assertFalse(Notification.objects.filter(event_id='eventtest', username='participant1').exists())