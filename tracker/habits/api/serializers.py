from rest_framework import serializers
from habits.models import Habit, HabitStatus

class HabitStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitStatus
        fields = ['is_completed', 'date']
        
class HabitSerializer(serializers.ModelSerializer):
  goal = serializers.CharField(
    source = "goal.name",
    read_only= True,
    required=False,)
  habit_statuses = HabitStatusSerializer(many=True, read_only=True)
  class Meta:
    model = Habit
    fields = ['name','goal','habit_statuses']