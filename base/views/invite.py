from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from ..models import Notification, Event, EventUser
from ..serializers import NotificationSerializer

#Post Request invites users
class Invite(CreateAPIView):
    def create(self, request, *args, **kwargs):
        # Extracting data from request and checking missing information
        entire_data = request.data
        username = entire_data.get("username")
        event_id = entire_data.get("event_id")
        name = entire_data.get("name")
        if not username or not event_id or not name:
            return JsonResponse({'error':'Missing Input'}, status=400)
        
        if username in EventUser.objects.filter(event_id = event_id).values_list('username', flat=True):
            return JsonResponse({'error':'User already in event'}, status=400)
        invite_info = {
            'event_id' : event_id,
            'username' : username,
            'notification' : f"You have been invited to {name}"
        }
        invite_serializer = NotificationSerializer(data=invite_info)
        if invite_serializer.is_valid():
            invite_serializer.save()
        else:
            return JsonResponse(invite_serializer.errors, status=400)
        return JsonResponse({"status":"success"}, status=200)
