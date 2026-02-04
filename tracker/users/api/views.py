from django.contrib.auth  import get_user_model
from rest_framework import viewsets
from .serializer import UserSerializer

User = get_user_model()
class UserApiView(viewsets.ReadOnlyModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  