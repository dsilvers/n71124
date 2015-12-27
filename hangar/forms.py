from django import forms

class SensorForm(forms.Form):
    serial = forms.CharField(max_length=60)
    value = forms.DecimalField(max_digits=5, decimal_places=2)


class SwitchStatusForm(forms.Form):
    serial = forms.CharField(max_length=60)


class ScheduleForm(forms.Form):
    departure = forms.DateTimeField()
    comment = forms.CharField(max_length=255, required=False)
    heater_on = forms.DateTimeField()
    heater_off = forms.DateTimeField()
