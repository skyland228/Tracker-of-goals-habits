from django.contrib.auth  import get_user_model
from rest_framework import viewsets, status
from .serializer import UserSerializer, TelegramConnectSerializer, StatisicsSerializer
from rest_framework.views import APIView
from users.models import TelegramLinkToken
from django.utils import timezone
from rest_framework.response import Response
from users.services.general_service import StatsService

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

    token_obj = TelegramLinkToken.objects.filter(token=token).first()
    print("HIT TELEGRAM CONNECT VIEW")
    if not token_obj:
        return Response(
            {"detail": "token not found"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if token_obj.used:
        return Response(
            {"detail": "token already used"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if token_obj.expires_at <= timezone.now():
        return Response(
            {"detail": "token expired"},
            status=status.HTTP_400_BAD_REQUEST
        )
    user = token_obj.user
    user.telegram_id = telegram_id
    user.save()
    token_obj.used = True
    token_obj.save()

    return Response(
      {"detail": "ok"},
      status=status.HTTP_200_OK)

class StatisticApiView(viewsets.ViewSet):
   def list(self,request):
    telegram_id = request.GET.get('telegram_id')
    if not telegram_id:
        user = request.user
        result = StatsService.calculate_stats(user)
        serializer = StatisicsSerializer(instance = result)
        return Response(serializer.data)
    user = User.objects.get(telegram_id = telegram_id)
    result = StatsService.calculate_stats(user)
    serializer = StatisicsSerializer(instance = result)
    return Response(serializer.data)