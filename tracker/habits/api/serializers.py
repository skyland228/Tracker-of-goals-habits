from rest_framework import serializers
from habits.models import Habit

class HabitSerializer(serializers.ModelSerializer):
  goal = serializers.CharField(
    source = "goal.name",
  )
  class Meta:
    model = Habit
    fields = ['name','goal']