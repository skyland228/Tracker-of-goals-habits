from rest_framework import viewsets
from habits.models import Habit
from .serializers import HabitSerializer

class HabitApiView(viewsets.ModelViewSet):
  queryset = Habit.objects.all()
  serializer_class = HabitSerializer

