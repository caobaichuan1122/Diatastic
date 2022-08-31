from django import forms

class AddNewProduct(forms.Form):

    blood_sugar_level = forms.DecimalField(label="Blood Sugar Level", max_digits=2, help_text="Enter Number",
                                       widget=forms.NumberInput(attrs={'class': 'form-control'}))
    diary_menu = forms.CharField(label="Menu", max_length=256,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    diary_date = forms.DateField(label="Date",
                                       widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}))
    diary_time = forms.TimeField(label="Time",
                                       widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}))
