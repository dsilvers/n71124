from django import forms

class SensorForm(forms.Form):
    serial = forms.CharField(max_length=60)
    value = forms.DecimalField(max_digits=5, decimal_places=2)

class SwitchStatusForm(forms.Form):
    serial = forms.CharField(max_length=60)