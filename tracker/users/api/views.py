from django.contrib.auth  import get_user_model
from rest_framework import viewsets, status
from .serializer import UserSerializer, TelegramConnectSerializer
from rest_framework.views import APIView
from users.models import TelegramLinkToken
from django.utils import timezone
from rest_framework.response import Response

User = get_user_model()
class UserApiView(viewsets.ReadOnlyModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  
class TelegramConnectView(APIView):
  def post(self,request):
    serializer = TelegramConnectSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)
    token = serializer.validated_data["token"]
    telegram_id = serializer.validated_data["telegram_id"]

    token_obj = TelegramLinkToken.objects.filter(
      token = token,
      used = False,
      expires_at__gt = timezone.now()).first()
    if not token_obj:
      return Response(
        {"detail": "invalid token"},
        status =status.HTTP_400_BAD_REQUEST)
    user = token_obj.user
    user.telegram_id = telegram_id
    user.save()
    token_obj.used = True
    token_obj.save()

    return Response(
      {"detail": "ok"},
      status=status.HTTP_200_OK)
