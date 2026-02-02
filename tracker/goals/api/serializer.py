from rest_framework import serializers
from goals.models import TemporalGoal, GeneralGoal

class TemporalGoalSerializer(serializers.ModelSerializer):
  class Meta:
    model = TemporalGoal
    fields = '__all__'

class GeneralGoalSerializer(serializers.ModelSerializer):
  class Meta:
    model = GeneralGoal
    fields = ['name','theme','user']
    