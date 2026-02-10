from rest_framework import serializers
from goals.models import TemporalGoal, GeneralGoal

class TemporalGoalSerializer(serializers.ModelSerializer):
  goal = serializers.CharField(
    source = 'general_goal.name',
    read_only = True,
    allow_null = True,)
  class Meta:
    model = TemporalGoal
    fields = ['name','deadline','is_completed','goal']

class GeneralGoalSerializer(serializers.ModelSerializer):
  class Meta:
    model = GeneralGoal
    fields = ['name','theme','user']
    