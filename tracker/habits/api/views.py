from rest_framework import viewsets
from habits.models import Habit, HabitStatus
from .serializers import HabitSerializer, HabitStatusSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from django.utils import timezone
from habits.services.habit_service import HabitServices
from rest_framework.response import Response

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

  @action(detail =True,methods = ['post'])
  def toggle_status(self,request, pk = None):
    telegram_id = request.GET.get('telegram_id')
    user = User.objects.get(telegram_id=telegram_id)
    habit = self.get_object()
    HabitServices.ensure_habit_statuses_exist(habit.user)
    status = HabitStatus.objects.get(
      habit = habit,
      date = timezone.localdate())
    HabitServices.change_status(status)
    return Response({
    "is_completed": status.is_completed})

class HabitStatusApiView(viewsets.ModelViewSet):
  serializer_class = HabitStatusSerializer
  queryset = HabitStatus.objects.all()

