from django import forms
from .models import TemporalGoal, GeneralGoal


class AddTgoal(forms.ModelForm):
    class Meta:
        model = TemporalGoal
        fields = ['name','deadline','general_goal']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'name-form'}),
            'deadline': forms.DateInput(attrs={'type': 'date','class': 'deadline-form'}),
            'general_goal': forms.Select(attrs={'class': 'select-form'})
        }
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args,**kwargs)

        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if TemporalGoal.objects.filter(user = self.user, name = name).exists():
            raise forms.ValidationError("Такая подцель уже существует")
        return name
        
class AddGeneralGoal(forms.ModelForm):
    class Meta:
        model = GeneralGoal
        fields = ['name', 'description', 'theme']
        widgets = {
            'theme': forms.Select(attrs={'class': 'theme-form'}),
            'name': forms.TextInput(attrs={'class': 'name-form'}),
            'description': forms.Textarea(attrs={'class': 'description-form'})
        }
    def __init__(self,*args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args,**kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if GeneralGoal.objects.filter(user = self.user, name=name).exists():
            raise forms.ValidationError("Имя должно быть уникальным")
        return name
