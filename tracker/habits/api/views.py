from rest_framework import viewsets
from habits.models import Habit, HabitStatus
from .serializers import HabitSerializer, HabitStatusSerializer
from django.contrib.auth import get_user_model

User = get_user_model()
class HabitApiView(viewsets.ModelViewSet):
  serializer_class = HabitSerializer

  def get_queryset(self):
    telegram_id = self.request.GET.get('telegram_id')
    if not telegram_id:
      return Habit.objects.filter(user = self.request.user)
    return Habit.objects.filter(user__telegram_id=telegram_id)
  
  def perform_create(self, serializer):
    telegram_id = self.request.query_params.get('telegram_id')
    if telegram_id:
      user = User.objects.get(telegram_id = telegram_id)
      serializer.save(user = user)

class HabitStatusApiView(viewsets.ModelViewSet):
  serializer_class = HabitStatusSerializer
  queryset = HabitStatus.objects.all()
  