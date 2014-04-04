from django import forms
from django.forms import widgets

class UIDateWidget(forms.DateInput):
    def __init__(self, attrs={}, format='%Y-%m-%d'):
        super(UIDateWidget, self).__init__(attrs={'class': 'uiDateField', 'size': '10'}, format=format)