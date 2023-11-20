from rest_framework.test import APITestCase
from base.models import user, Event
from .common_methods import checker


# Test class that unit tests the create event endpoint
# Testing:
# create event success (status, response, model), create event failures (status, response)
class CreateEventTest(APITestCase):
    def setUp(self):
        self.host = user.objects.create(username = "eventtestuser", password = "success")
        self.participant1 = user.objects.create(username = "participant1", password = "success")
        self.participant2 = user.objects.create(username = "participant2", password = "success")
        self.eventInfo = {
            "event": {
                "primary_date" : "2023-11-01",
                "name" : "originaltest",
                "host" : "eventtestuser"
            },
            "user": [
                "participant1",
                "participant2"
            ],
            "date": [
                "2023-08-23",
                "2023-11-23"
            ]
        }
        
    def test_event_success(self):
        response = self.client.post('/event/create/', data=self.eventInfo, format="json")
        # checks response and status
        checker(self, response, {'status': 'success'}, 200)
        # checks existence in model
        self.assertTrue(Event.objects.filter(host=self.host).exists())
    
    def test_event_input_failure(self):
        del self.eventInfo["user"]
        
        response = self.client.post('/event/create/', data=self.eventInfo, format="json")
        checker(self, response, {'error': "Missing Input"}, 400)
        
        self.eventInfo["user"] = ["participant1",
                                  "participant2"]
        
    def test_event_no_user_failure(self):
        self.eventInfo["user"].append("imaginaryfriend")
        
        response = self.client.post('/event/create/', data=self.eventInfo, format="json")
        # checks response and status
        checker(self, response, {'error': 'User(s) Not Found!'}, 400)
        
        self.eventInfo["user"].pop()
        
    def test_event_wrong_date_failure(self):
        self.eventInfo["date"].append("2023--05")
        
        response = self.client.post('/event/create/', data=self.eventInfo, format="json")
        checker(self, response, {'error': "Date Input Error!"}, 400)
        
        self.eventInfo["date"].pop()
    
    def test_event_no_host_failure(self):
        self.eventInfo["event"]["host"] = "imaginaryhost"
        
        response = self.client.post('/event/create/', data=self.eventInfo, format="json")
        checker(self, response, {'error': "Invalid Event Info"}, 400)

        self.eventInfo["event"]["host"] = "eventtestuser"
    
    def test_event_same_name(self):
        Event.objects.create(event_id= "eventtest",
                             name= "originaltest",
                             primary_date= "2023-11-01",
                             host= self.host)

        response = self.client.post('/event/create/', data=self.eventInfo, format="json")
        checker(self, response, {'error': "That event name is currently being used by you, please try another name!"}, 400)