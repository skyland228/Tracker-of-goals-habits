from django import forms
from .models import TemporalGoal, GeneralGoal, Theme


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

class CreateTheme(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'})
        }