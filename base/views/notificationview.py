from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from ..models import Notification

# Get Request that shows a user's notifications
class NotificationView(ListAPIView):
    def list(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if username is None:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        notifs = Notification.objects.filter(username=username).values()
        return JsonResponse(list(notifs), safe=False, status=200)