from rest_framework.test import APITestCase
from base.models import Notification, user, Event

class NotificationTest(APITestCase):
    def setUp(self):
        self.user = user.objects.create(username = "notification", password = "success")
        self.event_instance = Event.objects.create(event_id= "testevent",
                                              name= "testname",
                                              primary_date= "2023-03-23",
                                              host= self.user)
    def test_notification_failure(self):
        response = self.client.get('/notification/', data={"username": "notification"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
        
    def test_notification_success(self):
        Notification.objects.create(id = 439854,
                                    event_id = self.event_instance,
                                    username = self.user,
                                    notification = "testing notif")
        response = self.client.get('/notification/', data={"username": "notification"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'event_id_id': 'testevent',
                                            'id': 439854,
                                            'notification': 'testing notif',
                                            'username_id': 'notification'}])
        self.assertTrue(Notification.objects.filter(username='notification').exists())