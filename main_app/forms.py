#main_app/forms.py
from django import forms
from .models import Care

class CareForm(forms.ModelForm):
    class Meta:
        model = Care
        fields = ['date', 'action']
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            )
        }
