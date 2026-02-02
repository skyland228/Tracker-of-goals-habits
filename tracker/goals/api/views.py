from goals.models import TemporalGoal, GeneralGoal
from rest_framework import viewsets
from .serializer import TemporalGoalSerializer, GeneralGoalSerializer

class GeneralGoalViewSet(viewsets.ModelViewSet):
  queryset = GeneralGoal.objects.all()
  serializer_class = GeneralGoalSerializer

class TemporalGoalViewSet(viewsets.ModelViewSet):
  queryset = TemporalGoal.objects.all()
  serializer_class = TemporalGoalSerializer