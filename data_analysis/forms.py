# data_analysis/forms.py
from django import forms


class DataForm(forms.Form):
    file = forms.FileField()
    question = forms.CharField(max_length=200)
