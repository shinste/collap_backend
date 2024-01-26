from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from ..models import Notification

# Get Request that shows a user's notifications
class NotificationView(ListAPIView):
    def list(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if not username:
            return JsonResponse({'error':'Missing Input'}, status=400)

        notifs = Notification.objects.filter(username=username).values()

        def sort_key(notif):
            notification_content = notif.get('notification', '')
            if 'You must vote on' in notification_content or 'You have been invited' in notification_content:
                return 0  # Assign a lower value for notifications containing specific phrases
            else:
                return 1  # Assign a higher value for other notifications

        sorted_notifs = sorted(notifs, key=sort_key)


        return JsonResponse(list(sorted_notifs), safe=False, status=200)