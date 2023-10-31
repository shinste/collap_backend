from rest_framework.generics import CreateAPIView
from ..serializers import *

class pushVote(CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
