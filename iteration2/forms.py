from django import forms

from django import forms
from .models import Diary_Menu, Category, Portion
import datetime as dt

class DiaryForm(forms.ModelForm):
    date = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date',
                                                           'max': dt.datetime.today().date()}))
    time = forms.TimeField(widget=forms.NumberInput(attrs={'type': 'time'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    blood_sugar_level = forms.DecimalField(max_digits=3,
                                           decimal_places=1)
    portion = forms.ModelChoiceField(queryset=Portion.objects.all())
    class Meta:
        model = Diary_Menu
        fields = '__all__'
        exclude = ('diary', 'carbohydrates')

class UserForm(forms.Form):
    username = forms.CharField(label="user", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="password", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class DateForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))