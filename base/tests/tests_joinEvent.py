from rest_framework.test import APITestCase
from base.models import user, Event, EventDate, UserEvent, Availability, Notification

class JoinEventTest(APITestCase):
    def setUp(self):
        self.host = user.objects.create(
            username="user",
            password="password"
        )
        self.participant = user.objects.create(
            username="participant",
            password="password1"
        )
        self.event = Event.objects.create(
            event_id="testevent",
            primary_date="2023-10-12",
            name="event",
            host=self.host
        )

    def test_event_exist_success(self):
        data = {
            'username': self.participant.username,
            'event_id': self.event.event_id,
            'dates': ["2023-10-12", "2023-10-13", "2023-10-14"]
        }
        self.assertTrue(Event.objects.filter(event_id=data['event_id']).exists())

    def test_event_exist_fail(self):
        data = {
            'username': self.participant.username,
            'event_id': 'nonexistentevent',
            'dates': ["2023-10-12", "2023-10-13", "2023-10-14"]
        }
        response = self.client.post('/event/join_event/', data, format="json")
        self.assertEqual(response.json(), {'error': 'Event not found'})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Event.objects.filter(event_id=data['event_id']).exists())

    def test_create_user_event_success(self):
        data = {
            'username': self.participant.username,
            'event_id': self.event.event_id,
            'dates': ["2023-10-12", "2023-10-13", "2023-10-14"]
        }
        response = self.client.post('/event/join_event/', data, format="json")
        self.assertTrue(UserEvent.objects.filter(username=data['username'], event_id=self.event).exists())

    def test_create_user_event_fail(self):
        invalid_user_event_data = {
            'username': self.participant.username
        }
        response = self.client.post('/event/join_event/', invalid_user_event_data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(UserEvent.objects.filter(username=self.participant.username).exists())

    def test_event_date_success(self):
        data = {
            'username': self.participant.username,
            'event_id': self.event.event_id,
            'dates': ["2023-10-12", "2023-10-13", "2023-10-14"]
        }
        response = self.client.post('/event/join_event/', data, format="json")
        event_dates = EventDate.objects.filter(event_id=self.event.event_id)
        self.assertTrue(event_dates.exists())
        for date in data['dates']:
            self.assertTrue(event_dates.filter(date=date).exists())

    def test_event_date_fail(self):
        invalid_data = {
            'username': self.participant.username,
            'event_id': self.event.event_id,
            'dates': ["2023-10-12", "2023-10-13", "2023-10-1"]
        }
        response = self.client.post('/event/join_event/', invalid_data, format="json")
        self.assertEqual(response.status_code, 400)
