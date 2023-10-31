from django.http import JsonResponse
import json
from django.db.models import Count
from ..models import *

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
