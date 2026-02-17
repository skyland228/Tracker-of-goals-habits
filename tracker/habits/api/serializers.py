from rest_framework import serializers
from habits.models import Habit, HabitStatus

class HabitStatusSerializer(serializers.ModelSerializer):
    habit_name = serializers.CharField(source='habit.name', read_only=True)
    class Meta:
        model = HabitStatus
        fields = ['id','is_completed', 'date', 'habit_name']
        
class HabitSerializer(serializers.ModelSerializer):
  goal = serializers.CharField(
    source = "goal.name",
    read_only= True,
    required=False,)
  habit_statuses = HabitStatusSerializer(many=True, read_only=True)
  class Meta:
    model = Habit
    fields = ['id','name','goal','habit_statuses']