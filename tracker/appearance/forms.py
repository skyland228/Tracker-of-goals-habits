from django import forms
from .models import Theme

class CreateTheme(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'})
        }