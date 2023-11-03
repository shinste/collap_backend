from rest_framework.generics import CreateAPIView
from ..serializers import *

class PushVote(CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
