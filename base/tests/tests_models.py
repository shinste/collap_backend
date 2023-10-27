from django.test import TestCase
from base.models import *
import datetime
# Create your tests here.

class UserModelTests(TestCase):
    def setUp(self):
        user.objects.create(username = "xx", password = "xxx")
    def test_returns_username(self):
        example_user = user.objects.get(username = "xx")
        self.assertEquals(example_user.__str__(), "xx")
class EventModelTests(TestCase):
    def setUp(self):
        user.objects.create(username = "xx", password = "xxx")
        Event.objects.create(name="event1", event_id="example", primary_date=datetime.date.today(), host = user.objects.get(username = "xx"))
    def test_returns_name(self):
        example_event = Event.objects.get(event_id="example")
        self.assertEquals(example_event.__str__(), "event1")
    def test_host_name(self):
        example_event = Event.objects.get(event_id="example")
        self.assertEquals(example_event.host.__str__(), "xx")
    

        