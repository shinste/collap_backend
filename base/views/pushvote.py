from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from ..models import Notification, Event, EventUser, Vote
from ..serializers import NotificationSerializer

#Post Request invites users
class PushVote(CreateAPIView):
    def create(self, request, *args, **kwargs):
        # Extracting data from request and checking missing information
        entire_data = request.data
        event_id = entire_data.get("event_id")
        if not event_id:
            return JsonResponse({'error':'Missing Input'}, status=400)
        # updating status of voting event
        status =  Event.objects.get(event_id=event_id)
        status.voting = 'yes'
        status.save()

        #deleting all current votes for that event
        votes = Vote.objects.filter(event_id=event_id)
        for vote in votes:
            vote.delete()

        # notifying all participants that they must vote
        participants = EventUser.objects.filter(event_id=event_id).values_list('username', flat=True)
        for participant in participants:
            if not Notification.objects.filter(username = participant, event_id=event_id, notification=f"You must vote on date for {status.name}").exists():
                notif_data = {
                    'username' : participant,
                    'event_id' : event_id,
                    'notification' : f"You must vote on date for {status.name}"
                }
                notif_instance = NotificationSerializer(data=notif_data)
                if notif_instance.is_valid():
                    notif_instance.save()
                else:
                    return JsonResponse({"error":str(notif_instance.errors)}, status=400)
        return JsonResponse({"status":"success"}, status=200)