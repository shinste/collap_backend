from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from ..models import Availability

# Get Request that ranks the possible dates for an event and shows who is excluded from
# each date
class RankDates(ListAPIView):
    def list(self, request, *args, **kwargs):
        event_id = request.GET.get('event_id')
        if event_id is None:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        availability = Availability.objects.filter(event_id_id=event_id).values()
        ranked = {}
        participants = list(Availability.objects.filter(event_id_id=event_id).values_list('username_id', flat=True).distinct())
        # goes through each availability and removes user if they are available for that date
        for entry in availability:
            date = str(entry['date'])
            if date not in ranked.keys():
                ranked[date] = participants.copy()
            ranked[date].remove(entry['username_id'])
        # sorts dictionary keys (dates) from least amount of unavailable participants to most
        sorted_dates = sorted(ranked, key=lambda k: len(ranked[k]), reverse=False)
        return JsonResponse({key: ranked[key] for key in sorted_dates}, safe=False, status=200)
