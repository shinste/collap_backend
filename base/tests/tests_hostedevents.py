from rest_framework.test import APITestCase
from base.models import user, Event
from .common_methods import checker

# Test class that unit tests the hosted events endpoint
# Testing:
# hosted event success (status, response), hosted event failure (status, response)
class HostedEventsTest(APITestCase):
    def setUp(self):
        self.host = user.objects.create(username = "eventtestuser", password = "success")
        Event.objects.create(event_id= "eventtest",
                             name= "originaltest",
                             primary_date= "2023-11-01",
                             host= self.host)
        
    def test_hosted_event_success(self):
        response = self.client.get('/hosted/', data={'username': 'eventtestuser'})
        checker(self, response, [{"event_id": "eventtest", "primary_date": "2023-11-01",
                                  "name": "originaltest", "host_id": "eventtestuser"}], 200)
    
    def test_hosted_event_failure(self):
        response = self.client.get('/hosted/', data={})
        checker(self, response, {'error': 'Missing Input'}, 400)