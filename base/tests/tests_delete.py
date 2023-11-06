from rest_framework.test import APITestCase
from base.models import Notification, user, Event, EventUser, Availability, Vote, EventDate
from .common_methods import checker

# Test class that unit tests the Delete endpoint
# Testing:
# delete success (status, response, model), delete failure (status, response)
class DeleteTest(APITestCase):
    def setUp(self):
        host_instance = user.objects.create(username = "eventtestuser", password = "success")
        participant1 = user.objects.create(username = "participant1", password = "success")
        event_instance = Event.objects.create(event_id= "eventtest", name= "originaltest",
                                              primary_date= "2023-11-01", host= host_instance)
        EventUser.objects.create(username = participant1, event_id = event_instance)
        Availability.objects.create(username = participant1, event_id = event_instance, date = '2023-03-01')
        Notification.objects.create(event_id = event_instance, username = host_instance, notification = "testing notif")
        Vote.objects.create(username = participant1, event_id = event_instance, 
                            date = '2023-03-01')
        EventDate.objects.create(event_id = event_instance, date = '2023-03-01')
    
    def test_delete_input_failure(self):
        response = self.client.post('/event/delete/', data ={})
        checker(self, response, {'error':'Missing Input'}, 400)
        
    def test_delete_event_failure(self):
        response = self.client.post('/event/delete/', data ={'event_id' : "imaginaryevent",
                                                             'username': "eventtestuser"})
        checker(self, response, {'error': "Event not found"}, 400)
    
    def test_delete_host_failure(self):
        response = self.client.post('/event/delete/', data ={'event_id' : "eventtest",
                                                             'username': "nothost"})
        checker(self, response, {'error': "You don't have the authority to delete this event!"}, 400)
    
    def test_delete_success(self):
        response = self.client.post('/event/delete/', data ={'event_id' : "eventtest",
                                                             'username': "eventtestuser"})
        checker(self, response, {"status":"success"}, 200)
        # checking if all traces of deleted event are deleted
        self.assertFalse(Event.objects.filter(event_id="eventtest").exists())
        self.assertFalse(EventUser.objects.filter(event_id="eventtest").exists())
        self.assertFalse(Availability.objects.filter(event_id="eventtest").exists())
        self.assertFalse(Notification.objects.filter(event_id="eventtest").exists())
        self.assertFalse(Vote.objects.filter(event_id="eventtest").exists())
        self.assertFalse(EventDate.objects.filter(event_id="eventtest").exists())