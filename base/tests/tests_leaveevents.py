from rest_framework.test import APITestCase
from base.models import Notification, user, Event, EventUser, Availability, Vote
from .common_methods import checker

# Test class that unit tests the Leave Event endpoint
# Testing:
# leave event success (status, response, model), leave event failure (status, response)
class LeaveEventTest(APITestCase):
    def setUp(self):
        host_instance = user.objects.create(username = "eventtestuser", password = "success")
        participant1 = user.objects.create(username = "participant1", password = "success")
        event_instance = Event.objects.create(event_id= "eventtest", name= "originaltest",
                                              primary_date= "2023-11-01", host= host_instance)
        EventUser.objects.create(username = participant1, event_id = event_instance)
        Availability.objects.create(username = participant1, event_id = event_instance, date = '2023-03-01')
        Notification.objects.create(event_id = event_instance, username = host_instance, notification = "testing notif")
    
    def test_leave_event_success(self):
        response = self.client.post('/event/leave/',data ={'event_id' : "eventtest",
                                                           'username': "participant1"})
        checker(self, response, {"status":"success"}, 200)
        self.assertFalse(EventUser.objects.filter(username="participant1",
                                                  event_id = "eventtest").exists())
        self.assertFalse(Availability.objects.filter(username="participant1",
                                                     event_id = "eventtest").exists())
        self.assertFalse(Vote.objects.filter(username="participant1",
                                             event_id = "eventtest").exists())
        self.assertEqual(Notification.objects.filter(username="participant1",
                                                     event_id = "eventtest").first().notification,
                                                     "You are no longer in the event: originaltest!")
    
    def test_leave_event_missing_failure(self):
        response = self.client.post('/event/leave/', data={"event_id": "", "username": ""})
        checker(self, response, {"error":"Missing Input"}, 400)
    
    def test_leave_event_participant_failure(self):
        response = self.client.post('/event/leave/', data={'event_id' : "eventtest", 'username' : "ghost"})
        checker(self, response, {"error":"Participant already not in Event"}, 400)
        
    def test_leave_event_host_failure(self):
        response = self.client.post('/event/leave/', data={'event_id' : "eventtest", 'username': "eventtestuser"})
        checker(self, response, {'error':'The Host cannot leave the Event, Try deleting the Event instead!'}, 400)
        