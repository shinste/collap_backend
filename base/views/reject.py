from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from ..models import Notification

#Post Request that rejects an invite to an event and removes the notification
class Reject(CreateAPIView):
    def create(self, request, *args, **kwargs):
        # Extracting data from request and checking missing information
        try:
            entire_data = request.data
            username = entire_data.get("username")
            event_id = entire_data.get("event_id")
        except:
            return JsonResponse({'error':'Missing Input'}, status=400)
        notification_instance = Notification.objects.filter(event_id=event_id, username=username)
        if not notification_instance:
            return JsonResponse({'error': "No notification found for this event/participant."}, status=400)
        notification_instance.delete()
        return JsonResponse({"status":"success"}, status=200)
