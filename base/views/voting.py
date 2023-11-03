from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from ..models import Notification, EventUser, Event
from ..serializers import EventVoteSerializer


class Voting(CreateAPIView):
    def create(self, request, *args, **kwargs):
        # Extracting data from request and checking missing information
        try:
            entire_data = request.data
            username = entire_data.get("username")
            event_id = entire_data.get("event_id")
        except:
            return JsonResponse({'error':'Missing Input'}, status=400)
        # Precheck: checks if notification is present
        notification_instance = Notification.objects.filter(username=username, event_id=event_id)
        if not notification_instance:
            return JsonResponse({'error':'Sorry, we cannot find this notification!'}, status=400)
        # Precheck: checks if user is in event
        event_participants = EventUser.objects.filter(event_id=event_id).values_list('username', flat=True)
        if username not in event_participants:
            notification_instance.delete()
            return JsonResponse({'error':'Sorry, either you were kicked from this event or you were never apart of it!'}, status=400)
        # Precheck: checks if event exists
        event_instance = Event.objects.get(event_id=event_id)
        if not event_instance:
            notification_instance.delete()
            return JsonResponse({'error':'Sorry, this event no longer exists!'}, status=400)
        # Adding the vote to the vote table
        vote_instance = EventVoteSerializer(data=entire_data)
        if vote_instance.is_valid():
            vote_instance.save()
        else:
            return JsonResponse({'error': str(vote_instance.errors)})
        notification_instance.delete()
        return JsonResponse({'status': 'success'}, status=200)