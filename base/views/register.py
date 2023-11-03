from rest_framework.generics import CreateAPIView
from ..models import user
from ..serializers import UserSerializer
class Register(CreateAPIView):
    queryset = user.objects.all()
    serializer_class = UserSerializer