from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from hangar.forms import TemperatureForm
from hangar.models import Sensor, SensorData
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.

class TemperatureReportingView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TemperatureReportingView, self).dispatch(request, *args, **kwargs)

    def post(self,request):
        form = TemperatureForm(request.POST)
        if form.is_valid():
            try:
                sensor = Sensor.objects.get(serial=form.cleaned_data['serial'])
            except Sensor.DoesNotExist:
                return HttpResponse("Sensor Not Found")

            data = SensorData.objects.create(
                sensor=sensor,
                value=form.cleaned_data['temperature']
            )
            data.save()

            sensor.last_update = datetime.utcnow()
            sensor.last_value = form.cleaned_data['temperature']
            sensor.save()

            return HttpResponse("OK")
        else:
            return HttpResponse("Data is not valid - %s" % form.errors)

    def get(self,request):
        return HttpResponse("Use POST")



class FrontPageView(View):
    template_name = "base.html"
    def get(self, request):

        try:
            cowling = Sensor.objects.get(name="cowling")
            cowling_temp = int(9.0 / 5.0 * float(cowling.last_value) + 32.0)
        except Sensor.DoesNotExist:
            cowling_temp = "??"

        try:
            ambient = Sensor.objects.get(name="ambient")
            ambient_temp =  int(9.0 / 5.0 * float(ambient.last_value) + 32.0)
        except Sensor.DoesNotExist:
            ambient_temp = "??"

        return render(request, self.template_name, { "cowling": cowling_temp, "ambient": ambient_temp })