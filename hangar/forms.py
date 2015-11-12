from django import forms

class TemperatureForm(forms.Form):
    serial = forms.CharField(max_length=60)
    temperature = forms.DecimalField(max_digits=5, decimal_places=2)