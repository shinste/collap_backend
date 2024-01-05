from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from ..models import Event, EventUser

# Get Request that shows all the events a user is participating in
class GetEventInfo(ListAPIView):
    def list(self, request, *args, **kwargs):
        event_id = request.GET.get('event_id')
        if not event_id:
            return JsonResponse({'error':'Missing Input'})
        event = Event.objects.filter(event_id=event_id).values().first()
        all_users = list(EventUser.objects.filter(event_id=event_id).values_list('username', flat=True))
        event['participants'] = all_users
        return JsonResponse(event, safe=False, status=200)