from django.http import JsonResponse
from django.db.models import Count
from ..models import *
from rest_framework.generics import ListAPIView

class GetVotes(ListAPIView):
    def list(self, request, *args, **kwargs):
        event_id = request.GET.get('event_id')

        # Use Django's annotation to count votes per date for the given event_id
        vote_counts = (Vote.objects.filter(event_id=event_id).values('date').annotate(vote_count=Count('id')).order_by('date'))
        response_data = {
            'votes': [{'date': vote['date'], 'count': vote['vote_count']} for vote in vote_counts]
        }

        return JsonResponse(response_data, status=200)
