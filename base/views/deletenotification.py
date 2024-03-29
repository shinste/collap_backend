from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from ..models import Notification, Event

#Post Request that deletes notifications from an event
class DeleteNotifications(CreateAPIView):
    def create(self, request, *args, **kwargs):
        # Extracting data from request and checking missing information
        try:
            entire_data = request.data
            username = entire_data.get("username")
            event_id = entire_data.get("event_id")
            notification = entire_data.get("notification")
            if not username or not event_id or not notification:
                return JsonResponse({'error':'Missing Input'}, status=400)
            notification_instance = Notification.objects.filter(event_id=event_id, username=username, notification=notification)
            if not notification_instance:
                return JsonResponse({'error': "No notification found for this event/participant."}, status=400)
            notification_instance.delete()
            return JsonResponse({"status":"success"}, status=200)
        except Exception as error:
            return JsonResponse({'error': f'{error}'})

