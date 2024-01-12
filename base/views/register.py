from rest_framework.generics import CreateAPIView
from ..models import user
from ..serializers import UserSerializer
from django.views.decorators.csrf import ensure_csrf_cookie

# Post Request that creates a new user
class Register(CreateAPIView):
    queryset = user.objects.all()
    serializer_class = UserSerializer