from django import forms
from .models import HabitStatus


class HabitStatusForm(forms.ModelForm):
    class Meta:
        model = HabitStatus
        fields = ['is_completed']