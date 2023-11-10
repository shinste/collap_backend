from rest_framework.test import APITestCase
from base.models import Vote, user, Event

class GetVotesTest(APITestCase):
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

    def test_get_votes_success(self):
        Vote.objects.create(
            event_id=self.event,
            username=self.participant,
            date="2023-10-12"
        )

        response = self.client.get('/event/get_votes/', data={"event_id": "testevent"})
        self.assertEqual(response.status_code, 200)

        expected_data = {
            'votes': [{'date': '2023-10-12', 'count': 1}]
        }
        self.assertEqual(response.json(), expected_data)
        self.assertTrue(Vote.objects.filter(event_id="testevent", date="2023-10-12").exists())

    def test_get_votes_fail(self):
        response = self.client.get('/event/get_votes/', data={"event_id": "nonexist"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"votes": []})

