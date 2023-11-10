from rest_framework.test import APITestCase
from base.models import user, Event, Notification


class PushVoteTest(APITestCase):
    def setUp(self):
        self.user = user.objects.create(username = "user", password = "password")
        self.event_instance = Event.objects.create(
            event_id= "testevent",
            name= "testname",
            primary_date= "2023-03-23",
            host= self.user
        )
        self.participant = user.objects.create(
            username="participant",
            password="password1"
        )

        self.notif_data = {
            "event_id": "testevent",
            "username": "participant",
            "notification": "success notif"
        }

    def test_push_vote_success(self):
        response = self.client.post('/event/push_vote/', self.notif_data)

        self.assertEqual(response.status_code, 201)
        expected_response = {
            "event_id": "testevent",
            "username": "participant",
            "notification": "success notif"
        }

        # Event with have an id attatched to it but user will not use it
        actual_response = response.json()
        if 'id' in actual_response:
            del actual_response['id']

        self.assertEqual(actual_response, expected_response)
        self.assertTrue(Notification.objects.filter(event_id='testevent').exists())

    def test_push_vote_fail(self):
        response = self.client.post('/event/push_vote/', {})

        self.assertEqual(response.status_code, 400)

        expected_error_response = {
            "notification": ["This field is required."],
            "event_id": ["This field is required."],
            "username": ["This field is required."]
        }

        actual_error_response = response.json()

        self.assertEqual(actual_error_response, expected_error_response)
        self.assertFalse(Notification.objects.filter(event_id='testevent').exists())


  