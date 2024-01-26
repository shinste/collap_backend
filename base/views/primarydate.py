from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from ..models import Event
from datetime import datetime

# Post Request that changes the primary date of an event, only done by host
class PrimaryDate(CreateAPIView):
    def create(self, request, *args, **kwargs):
        # Extracting data from request and checking missing information
        entire_data = request.data
        event_id = entire_data["event_id"]
        date = entire_data["date"]
        if not event_id or not date:
            return JsonResponse({'error':'Missing Input'}, status=400)
        try:
            event = Event.objects.get(event_id = event_id)
        except:
            # Code below should theoretically never run but just in case
            return JsonResponse({'error':'No Event with this ID'}, status=400)
        
        # If primary date is the same as the proposed date, let user know
        date_check = datetime.strptime(date, "%Y-%m-%d").date()
        if date_check == event.primary_date:
            return JsonResponse({"error": "This was already the Primary Date for this Event"}, status=400)
        
        event.primary_date = date
        event.save()
        return JsonResponse({"status": 'success'}, status=200)