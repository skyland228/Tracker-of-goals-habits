from django import forms
from .models import HabitStatus, Habit, TemporalGoal, GeneralGoal


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

class AddGeneralGoal(forms.ModelForm):
    class Meta:
        model = GeneralGoal
        fields = ['name', 'description', 'theme']
        widgets = {
            'theme': forms.Select(attrs={'class': 'form-control'}),
        }