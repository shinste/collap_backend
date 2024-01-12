from rest_framework.generics import CreateAPIView
from ..models import user
from ..serializers import UserSerializer

from django.views.decorators.csrf import csrf_exempt
# Post Request that creates a new user
@csrf_exempt
class Register(CreateAPIView):
    queryset = user.objects.all()
    serializer_class = UserSerializer