from django import forms
from .models import HabitStatus, Habit, TemporalGoal


class HabitStatusForm(forms.ModelForm):
    class Meta:
        model = HabitStatus
        fields = ['is_completed']



class AddHabit(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name','goal']

class AddTgoal(forms.ModelForm):
    class Meta:
        model = TemporalGoal
        fields = ['name','deadline','general_goal']