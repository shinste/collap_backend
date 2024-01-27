from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from ..models import Notification, EventUser, Event
from ..serializers import EventVoteSerializer

# Post Request that creates voting records from a user that is prompted to vote
class Voting(CreateAPIView):
    def create(self, request, *args, **kwargs):
        # Extracting data from request and checking missing information
        entire_data = request.data
        username = entire_data.get("username")
        event_id = entire_data.get("event_id")
        dates = entire_data.get("dates")
        if not username or not event_id or not dates:
            return JsonResponse({"error":"Missing Input"},status=400)
        event_instance = Event.objects.filter(event_id=event_id).first()
        name = event_instance.name
        notification_instance = Notification.objects.filter(username=username, event_id=event_id, notification=f"You must vote on date for {name}")
        # Precheck: checks if event exists
        if not event_instance:
            if notification_instance:
                notification_instance.delete()
            return JsonResponse({'error':'Sorry, this event no longer exists!'}, status=400)
        # Precheck: checks if user is in event and if notification actually exists
        event_participants = EventUser.objects.filter(event_id=event_id).values_list('username', flat=True)
        if username not in event_participants:
            if notification_instance:
                notification_instance.delete()
            return JsonResponse({'error':'Sorry, either you were kicked from this event or you were never apart of it!'}, status=400)
        if not notification_instance:
            return JsonResponse({'error':'Sorry, we cannot find this notification!'}, status=400)
        # Adding the votes to the vote table
        for date in set(dates):
            each_vote = {
                'username': username,
                'event_id': event_id,
                'date': date
            }
            vote_instance = EventVoteSerializer(data=each_vote)
            if vote_instance.is_valid():
                vote_instance.save()
            else:
                return JsonResponse({'error': str(vote_instance.errors)}, status=400)
        notification_instance.delete()
        return JsonResponse({'status': 'success'}, status=200)