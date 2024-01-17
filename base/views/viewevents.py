from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from ..models import EventUser, Event, EventDate

# Get Request that shows all the events a user is participating in
class ViewEvents(ListAPIView):
    def list(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if not username:
            return JsonResponse({'error': 'Missing Input'}, status=400)
        events = EventUser.objects.filter(username=username).values_list('event_id', flat=True)
        participated_events = []
        for participating_id in events:
            all_events = list(Event.objects.filter(event_id = participating_id).values())
            participants = list(EventUser.objects.filter(event_id=participating_id).values_list('username', flat=True))
            all_events[0]["participants"] = participants
            dates = list(EventDate.objects.filter(event_id=participating_id).values_list('date', flat=True))
            all_events[0]["dates"] = dates
            participated_events.append(all_events[0])

        
        return JsonResponse(participated_events, safe=False, status=200)