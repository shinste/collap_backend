from rest_framework.test import APITestCase
from base.models import user, Event, EventDate, UserEvent, Availability, Notification

# class JoinEventTest(APITestCase):
#     def setUp(self):
#         self.host = user.objects.create(
#             username="user",
#             password="password"
#         )
#         self.participant = user.objects.create(
#             username="participant",
#             password="password1"
#         )
#         self.event = Event.objects.create(
#             event_id="testevent",
#             primary_date="2023-10-12",
#             name="event",
#             host=self.host
#         )

#     def test_get_event_success(self):
