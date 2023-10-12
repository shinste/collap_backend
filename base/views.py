from rest_framework import generics
from .models import *
from .serializers import *
from django.http import HttpResponse, JsonResponse
import json

class EventView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

def Homepage(request):
    return HttpResponse("Temporary Home Page")

def NotificationView(request):
    try: 
        json_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    name = json_data.get('username')
    notifs = Notification.objects.filter(username=name).values()
    return JsonResponse(list(notifs), safe=False, status=200)
    
    
