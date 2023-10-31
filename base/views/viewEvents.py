from ..models import *
from django.http import JsonResponse
from .constant.json_load import json_load

def viewEvents(request):
    json_data = json_load(request)

    username = json_data.get('username')

    # Filter UserEvent objects by username to get associated event_ids
    user_events = UserEvent.objects.filter(username=username)

    # Extract event_ids from user_events
    event_ids = [user_event.event_id.event_id for user_event in user_events]

    # Return a list of event_ids associated with the given username
    return JsonResponse({'event_ids': event_ids}, status=200)
