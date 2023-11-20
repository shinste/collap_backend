from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from ..models import Event

# Get Request that returns the events that a user is currently hosting
class HostedEvents(ListAPIView):
    def list(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if username is None:
            return JsonResponse({'error': 'Missing Input'}, status=400)

        hosted_events = Event.objects.filter(host=username).values()
        return JsonResponse(list(hosted_events), safe=False, status=200)