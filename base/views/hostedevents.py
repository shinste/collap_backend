from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from ..models import Event

class HostedEvents(ListAPIView):
    def list(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if username is None:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        hosted_events = Event.objects.filter(host=username).values()
        return JsonResponse(list(hosted_events), safe=False, status=200)