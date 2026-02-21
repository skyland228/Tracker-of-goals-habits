from rest_framework import serializers
from habits.models import Habit, HabitStatus
from django.utils import timezone

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
  today_status = serializers.SerializerMethodField()
  class Meta:
    model = Habit
    fields = ['id','name','goal','today_status']

  def get_today_status(self,obj):
    status = obj.habit_statuses.filter(date = timezone.localdate()).first()
    return status.is_completed if status else False