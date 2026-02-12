from rest_framework import viewsets
from habits.models import Habit
from .serializers import HabitSerializer
from django.utils import timezone

class HabitApiView(viewsets.ModelViewSet):
  serializer_class = HabitSerializer

  def get_queryset(self):
    telegram_id = self.request.GET.get('telegram_id')
    if not telegram_id:
      return Habit.objects.filter(user = self.request.user)
    return Habit.objects.filter(user__telegram_id=telegram_id)

