from rest_framework.test import APITestCase
from base.models import user, Event
from .common_methods import checker

# Test class that unit tests the Primary Date endpoint
# Testing:
# primary date success (status, response, model), leave event failure (status, response)
class PrimaryDateTest(APITestCase):
    def setUp(self):
        host_instance = user.objects.create(username = "eventtestuser", password = "success")
        Event.objects.create(event_id= "eventtest", name= "originaltest",
                             primary_date= "2023-11-01", host= host_instance)
    
    def test_primarydate_input_failure(self):
        response = self.client.post('/primary/', {})
        checker(self, response, {'error':'Missing Input'}, 400)
        
    def test_primarydate_success(self):
        response = self.client.post('/primary/', {'event_id' : 'eventtest', 'date' : '2023-01-03'})
        checker(self, response, {"status": 'success'}, 200)
        new_primary = str(Event.objects.get(event_id="eventtest").primary_date)
        self.assertEqual(new_primary, "2023-01-03")
    
    def test_primarydate_input_failure(self):
        response = self.client.post('/primary/', {'event_id' : 'imaginaryevent', 'date' : '2023-01-03'})
        checker(self, response, {'error':'No Event with this ID'}, 400)
    
    def test_primarydate_same_failure(self):
        response = self.client.post('/primary/', {'event_id' : 'eventtest', 'date' : '2023-11-01'})
        checker(self, response, {"error": "This was already the Primary Date for this Event"}, 400)