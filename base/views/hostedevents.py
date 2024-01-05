from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from ..models import Event, EventUser, EventDate

# Get Request that returns the events that a user is currently hosting
class HostedEvents(ListAPIView):
    def list(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if not username:
            return JsonResponse({'error': 'Missing Input'}, status=400)

        hosted_events = Event.objects.filter(host=username).values_list('event_id', flat=True)
        hosted = []
        for hosting_id in hosted_events:
            all_events = list(Event.objects.filter(event_id = hosting_id).values())
            participants = list(EventUser.objects.filter(event_id=hosting_id).values_list('username', flat=True))
            all_events[0]["participants"] = participants
            dates = list(EventDate.objects.filter(event_id=hosting_id).values_list('date', flat=True))
            all_events[0]["dates"] = dates
            hosted.append(all_events[0])


        return JsonResponse(hosted, safe=False, status=200)