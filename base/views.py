from rest_framework import generics
from rest_framework.generics import CreateAPIView
from .models import *
from .serializers import *
from django.http import HttpResponse, JsonResponse
import json
from django.db.models import Count

class EventView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

def Homepage(request):
    return HttpResponse("Temporary Home Page")

def notificationView(request):
    try:
        json_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    name = json_data.get('username')
    notifs = Notification.objects.filter(username=name).values()
    return JsonResponse(list(notifs), safe=False, status=200)

def viewEvents(request):
    try:
        json_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    username = json_data.get('username')

    # Filter UserEvent objects by username to get associated event_ids
    user_events = UserEvent.objects.filter(username=username)

    # Extract event_ids from user_events
    event_ids = [user_event.event_id.event_id for user_event in user_events]

    # Now, you have a list of event_ids associated with the given username
    return JsonResponse({'event_ids': event_ids}, status=200)


def getVotes(request):
    try:
        json_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    event_id = json_data.get('event_id')

    # Use Django's annotation to count votes per date for the given event_id
    vote_counts = (Vote.objects.filter(event_id=event_id).values('date').annotate(vote_count=Count('id')).order_by('date'))
    response_data = {
        'votes': [{'date': vote['date'], 'count': vote['vote_count']} for vote in vote_counts]
    }

    return JsonResponse(response_data, status=200)

class joinEvent(CreateAPIView):

    def create(self, request, *args, **kwargs):
        data = request.data
        user_data = data.get('username')
        event_id_data = data.get('event_id')
        date_data = data.get('dates')

        try:
            event = Event.objects.get(event_id=event_id_data)
            event_name = event.name
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)

       

        user_event_data = {
            'username': user_data,
            'event_id': event_id_data
        }

        # Create the UserEvent
        user_event_serializer = EventUserSerializer(data=user_event_data)
        if user_event_serializer.is_valid():
            user_event_serializer.save()
        else:
            return JsonResponse(user_event_serializer.errors, status=400)

        for date in date_data:
            if EventDate.objects.filter(event_id=event_id_data, date=date).exists():
                pass
            else:
                temp_date_data = {
                    'event_id': event_id_data,
                    'date': date
                }
                event_date_serializer = EventDateSerializer(data=temp_date_data)
                if event_date_serializer.is_valid():
                    event_date_serializer.save()
                else:
                    return JsonResponse(event_date_serializer.errors, status=400)

            if Availability.objects.filter(event_id=event_id_data, username=user_data, date=date).exists():
                continue
            availability_data = {
                'event_id': event_id_data,
                'username': user_data,
                'date': date
            }

            availability_date_serializer = EventAvailabilitySerializer(data=availability_data)
            if availability_date_serializer.is_valid():
                availability_date_serializer.save()
            else:
                return JsonResponse(availability_date_serializer.errors, status=400)

        if Notification.objects.filter(event_id=event_id_data, username=user_data).exists():
            notification_to_delete = Notification.objects.get(event_id=event_id_data, username=user_data)
            notification_to_delete.delete()
        return JsonResponse({'status': 'success'}, status=200)

class pushVote(CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    