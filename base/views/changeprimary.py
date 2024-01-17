from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from ..models import Notification, Event, EventUser, EventDate
from ..serializers import NotificationSerializer, EventDateSerializer

#Post Request invites users
class ChangePrimary(CreateAPIView):
    def create(self, request, *args, **kwargs):
        # Extracting data from request and checking missing information
        entire_data = request.data
        start = entire_data.get("start")
        end = entire_data.get("end")
        event_id = entire_data.get("event_id")
        primary = entire_data.get("primary")
        primary_end = entire_data.get('primary_end')
        if not start or not end or not event_id or not primary or not primary_end:
            return JsonResponse({'error':'Missing Input'}, status=400)

        changes = Event.objects.get(event_id=event_id)
        if changes.primary_date == primary:
            return JsonResponse({'error': 'Date already the Primary Date'}, status=400)
        else:
            changes.primary_date = primary
            changes.primary_end = primary_end
            changes.start = start
            changes.end = end
            changes.save()
        return JsonResponse({"status":"success"}, status=200)
