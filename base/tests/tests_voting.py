from rest_framework.test import APITestCase
from base.models import user, Event, EventUser, Notification, Vote
from .common_methods import checker

# Test class that unit tests the Voting endpoint
# Testing:
# voting success (status, response, model), registration failure (status, response)
class Voting(APITestCase):
    def setUp(self):
        host_instance = user.objects.create(username = "eventtestuser", password = "success")
        self.participant1 = user.objects.create(username = "participant1", password = "success")
        self.event = Event.objects.create(event_id= "eventtest", name= "originaltest",
                                          primary_date= "2023-11-01", host= host_instance)
        self.request_data = {'event_id' : 'eventtest',
                            'username' : 'participant1',
                            'date' : '2023-01-22'}
        
    def test_voting_no_input_failure(self):
        response = self.client.post('/vote/', data={})
        checker(self, response, {'error':'Missing Input'}, 400)
    
    def test_voting_participant_failure(self):
        # manually inserting notification objects due to the endpoint deleting notifications
        Notification.objects.create(event_id = self.event,
                                    username = self.participant1,
                                    notification = "Vote on Date for Test Event")
        
        response = self.client.post('/vote/', data=self.request_data)
        checker(self, response, {'error':'Sorry, either you were kicked from this event or you were never apart of it!'}, 400)

    def test_voting_success(self):
        Notification.objects.create(event_id = self.event,
                                    username = self.participant1,
                                    notification = "Vote on Date for Test Event")
        
        # adding the user to the event
        EventUser.objects.create(username = self.participant1, event_id = self.event)
        
        response = self.client.post('/vote/', data=self.request_data)
        checker(self, response, {'status': 'success'}, 200)
        self.assertTrue(Vote.objects.filter(username="participant1").exists())
    
    def test_voting_notification_failure(self):
        EventUser.objects.create(username = self.participant1, event_id = self.event)
        
        response = self.client.post('/vote/', data=self.request_data)
        checker(self, response, {'error':'Sorry, we cannot find this notification!'}, 400)
        
    def test_voting_event_failure(self):
        self.request_data["event_id"] = "imaginaryevent"
        
        response = self.client.post('/vote/', data=self.request_data)
        checker(self, response, {'error':'Sorry, this event no longer exists!'}, 400)