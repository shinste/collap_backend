from rest_framework.test import APITestCase
from base.models import Availability, user, Event, EventUser
from .common_methods import checker

# Test class that unit tests the Rank Dates endpoint
# Testing:
# rank dates success (status, response), rank dates failure (status, response)
class RankDatesTest(APITestCase):
    def setUp(self):
        self.host = user.objects.create(username = "eventtestuser", password = "success")
        self.participant1 = user.objects.create(username = "participant1", password = "success")
        self.participant2 = user.objects.create(username = "participant2", password = "success")
        event = Event.objects.create(event_id= "eventtest", name= "originaltest",
                                     primary_date= "2023-11-01", host= self.host)
        EventUser.objects.create(username = self.participant1, event_id = event)
        EventUser.objects.create(username = self.participant2, event_id = event)
        Availability.objects.create(username = self.participant1, event_id = event,
                                    date = "2023-03-01")
        Availability.objects.create(username = self.participant1, event_id = event,
                                    date = "2023-03-02")
        Availability.objects.create(username = self.participant1, event_id = event,
                                    date = "2023-03-03")
        Availability.objects.create(username = self.participant2, event_id = event,
                                    date = "2023-03-01")
    
    def test_rankdates_no_event_failure(self):
        response = self.client.get('/ranked/', data={})
        checker(self, response, {'error': 'Missing Input'}, 400)
        
    def test_rankdates_success(self):
        response = self.client.get('/ranked/', data={'event_id': "eventtest"})
        checker(self, response, {'2023-03-01': [], 
                                 '2023-03-02': ['participant2'], 
                                 '2023-03-03': ['participant2']}, 200)