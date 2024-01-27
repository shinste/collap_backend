from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from ..models import Event, EventUser, EventDate

# Get Request that returns the events that a user is currently hosting
class EventDates(ListAPIView):
    def list(self, request, *args, **kwargs):
        event_id = request.GET.get('event_id')
        if not event_id:
            return JsonResponse({'error': 'Missing Input'}, status=400)
        all_dates = list(EventDate.objects.filter(event_id=event_id).values_list('date', flat=True))
        return JsonResponse(all_dates, safe=False, status=200) 