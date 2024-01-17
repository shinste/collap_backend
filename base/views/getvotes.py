from django.http import JsonResponse
from django.db.models import Count
from ..models import *
from rest_framework.generics import ListAPIView

class GetVotes(ListAPIView):
    def list(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if not username:
            return JsonResponse({'error': 'Missing Input'}, status=400)

        events = Event.objects.filter(host=username).values_list('event_id', flat=True)
        # if not events:
        #     return JsonResponse
        response_data = {}
        for event_id in events:
            each_data = {
                'status' : 'Inactive'
            }
            if Event.objects.get(event_id=event_id).voting == 'yes':
                each_data['status'] = 'Active'
            # Use Django's annotation to count votes per date for the given event_id
            vote_counts = Vote.objects.filter(event_id=event_id).values('date').annotate(vote_count=Count('id')).order_by('date')
            each_data["dates"] = [vote['date'] for vote in vote_counts]
            each_data["votes"] = [{'data': [vote['vote_count'] for vote in vote_counts]}]


            participants = EventUser.objects.filter(event_id=event_id).values_list("username", flat=True)
            each_data["total_users"] = list(participants)

            waiting = Vote.objects.filter(event_id=event_id).values_list("username", flat=True)

            each_data["waiting"] = list(set(participants) - set(waiting))
            response_data[event_id] = each_data
        
        return JsonResponse(response_data, status=200)