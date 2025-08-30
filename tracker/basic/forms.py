from django import forms
from .models import HabitStatus, Habit


class HabitStatusForm(forms.ModelForm):
    class Meta:
        model = HabitStatus
        fields = ['is_completed']

class AddHabit(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name','goal']

