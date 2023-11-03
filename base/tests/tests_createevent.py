from rest_framework.test import APITestCase
from base.models import user, Event
from .common_methods import fail_check


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
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})
        self.assertTrue(Event.objects.filter(host=self.host).exists())
    
    def test_event_input_failure(self):
        holder = self.eventInfo["user"]
        
        del self.eventInfo["user"]
        
        fail_check(self, {'error': "Missing Information"})
        
        self.eventInfo["user"] = holder
        
    def test_event_no_user_failure(self):
        
        self.eventInfo["user"].append("imaginaryfriend")
        
        fail_check(self, {'error': 'User(s) Not Found!'})
        
        self.eventInfo["user"].pop()
        
    def test_event_wrong_date_failure(self):
        self.eventInfo["date"].append("2023--05")
        
        fail_check(self, {'error': "Date Input Error!"})
        
        self.eventInfo["date"].pop()
    
    def test_event_no_host_failure(self):
        self.eventInfo["event"]["host"] = "imaginaryhost"
        
        fail_check(self, {'error': "Invalid Event Info"})

        self.eventInfo["event"]["host"] = "eventtestuser"
    
    def test_event_same_name(self):
        Event.objects.create(event_id= "eventtest",
                             name= "originaltest",
                             primary_date= "2023-11-01",
                             host= self.host)

        fail_check(self, {'error': "That event name is currently being used by you, please try another name!"})