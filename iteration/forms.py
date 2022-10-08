from django import forms

from .models import Drink, Food
# Food_Choices = [(item.name, item.name) for item in Food.objects.all()]
# Drinks_Choices = [(item.name, item.name) for item in Drink.objects.all()]


class UserForm(forms.Form):
    username = forms.CharField(label="user", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="password", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class DiaryForm(forms.Form):

    date = forms.DateField(widget=forms.NumberInput(attrs={"type": "date"}))
    time = forms.TimeField(widget=forms.NumberInput(attrs={"type": "time"}))

    blood_sugar_level = forms.DecimalField(
        decimal_places=2,
        max_digits=5
    )

    # food_items = forms.MultipleChoiceField(choices=Food_Choices)
    # drinks = forms.MultipleChoiceField(choices=Drinks_Choices)