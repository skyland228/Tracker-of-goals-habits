from .models import HabitStatus, Habit
from django import forms

class HabitStatusForm(forms.ModelForm):
    class Meta:
        model = HabitStatus
        fields = ['is_completed']

class AddHabit(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name','goal']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'name-form'}),
            'goal': forms.Select(attrs={'class': 'select-form'})
        }
    def __init__(self,*args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args,**kwargs)
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Habit.objects.filter(user = self.user, name = name).exists():
            raise forms.ValidationError("Привычка с этим названием уже существует")
        return name