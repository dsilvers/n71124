from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from hangar.forms import TemperatureForm
from hangar.models import Sensor, SensorData
from datetime import datetime

# Create your views here.

class TemperatureReportingView(View):
    def post(self,request):
        form = TemperatureForm(request.POST)
        if form.is_valid():
            try:
                sensor = Sensor.objects.get(serial=form.cleaned_data['serial'])
            except Sensor.DoesNotExist:
                return HttpResponse("Sensor Not Found")

            data = SensorData.create(
                sensor=sensor,
                value=form.cleaned_data['temperature']
            )
            data.save()

            sensor.last_update = datetime.utcnow()
            sensor.last_data = data
            sensor.save()

            return HttpResponse("OK")