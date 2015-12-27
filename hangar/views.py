from django.shortcuts import render
from django.views.generic import View
from django.views.generic.edit import FormView
from django.http import HttpResponse
from hangar.forms import SensorForm, SwitchStatusForm, ScheduleForm
from hangar.models import Sensor, SensorData, PowerSwitch, PowerSchedule
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


# Create your views here.

class SensorReportingView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SensorReportingView, self).dispatch(request, *args, **kwargs)

    def post(self,request):
        form = SensorForm(request.POST)
        if form.is_valid():
            try:
                sensor = Sensor.objects.get(serial=form.cleaned_data['serial'])
            except Sensor.DoesNotExist:
                return HttpResponse("Sensor Not Found")

            data = SensorData.objects.create(
                sensor=sensor,
                value=form.cleaned_data['value']
            )
            data.save()

            sensor.last_update = datetime.utcnow()
            sensor.last_value = form.cleaned_data['value']
            sensor.save()

            return HttpResponse("OK")
        else:
            return HttpResponse("Data is not valid - %s" % form.errors)

    def get(self,request):
        return HttpResponse("Use POST")


class SwitchStatusView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SwitchStatusView, self).dispatch(request, *args, **kwargs)

    def post(self,request):
        form = SwitchStatusForm(request.POST)
        if form.is_valid():
            try:
                sensor = PowerSwitch.objects.get(serial=form.cleaned_data['serial'])
            except PowerSwitch.DoesNotExist:
                return HttpResponse("Switch Not Found")

            if sensor.status:
                return HttpResponse("ON")
            else:
                return HttpResponse("OFF")
        else:
            return HttpResponse("Data is not valid - %s" % form.errors)

    def get(self,request):
        return HttpResponse("Use POST")


class FrontPageView(View):
    template_name = "base.html"
    def get(self, request):

        try:
            heater_watts = Sensor.objects.get(name="Heater Watts")
        except Sensor.DoesNotExist:
            heater_watts = "???"
        try:
            heater_amps = Sensor.objects.get(name="Heater Amps")
        except Sensor.DoesNotExist:
            heater_amps = "???"

        try:
            cowling = Sensor.objects.get(name="Cowling")
            cowling_temp = int(9.0 / 5.0 * float(cowling.last_value) + 32.0)
        except Sensor.DoesNotExist:
            cowling = False
            cowling_temp = "??"

        try:
            ambient = Sensor.objects.get(name="Ambient")
            ambient_temp =  int(9.0 / 5.0 * float(ambient.last_value) + 32.0)
        except Sensor.DoesNotExist:
            ambient = False
            ambient_temp = "??"

        temps_since = datetime.now() - timedelta(hours=12)

        cowling_dates = []
        cowling_data = []
        ambient_dates = []
        ambient_data = []

        if cowling:
            sensor_data = SensorData.objects.filter(sensor=cowling, date__gt=temps_since).order_by("-date")[0:99]
            for data in sensor_data:
                cowling_dates.append(data.date.strftime("%Y-%m-%d %H:%M:%S"))
                cowling_data.append(float(data.value) * 1.8 + 32.0)
        if ambient:
            sensor_data = SensorData.objects.filter(sensor=ambient, date__gt=temps_since).order_by("-date")[0:99]
            for data in sensor_data:
                ambient_dates.append(data.date.strftime("%Y-%m-%d %H:%M:%S"))
                ambient_data.append(float(data.value) * 1.8 + 32.0)

        heater_status = PowerSwitch.objects.filter(serial="heater").first()
        if heater_status and heater_status.status:
            status = True
        else:
            status = False


        return render(request, self.template_name, { 
            "cowling": cowling_temp, 
            "ambient": ambient_temp,
            "cowling_dates": json.dumps(cowling_dates),
            "cowling_data": json.dumps(cowling_data),
            "ambient_dates": json.dumps(ambient_dates),
            "ambient_data": json.dumps(ambient_data),
            "heater_watts": heater_watts.last_value,
            "heater_amps": heater_amps.last_value,
            "heater_status": status,
        })


class ScheduleView(FormView):
    template_name = 'schedule.html'
    form_class = ScheduleForm
    success_url = '/schedule/'

    def get_initial(self):
        now = datetime.utcnow()
        discard = timedelta(minutes=now.minute % 15, seconds=now.second, microseconds=now.microsecond)
        now -= discard

        initial = {
            'departure': now,
            'heater_on': now - timedelta(hours=8),
            'heater_off': now + timedelta(hours=2),
        }
        return initial

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.get_initial())
        schedules = PowerSchedule.objects.all()
        return render(request, self.template_name, {'form': form, 'schedule': schedules })

    def form_valid(self, form):
        # yeah, someday we might have more than one?
        switch = PowerSwitch.objects.all().first()
        PowerSchedule(
            switch = switch,
            start = form.cleaned_data['heater_on'],
            end = form.cleaned_data['heater_off'],
            departure = form.cleaned_data['departure'],
            comment = form.cleaned_data['comment'],
        ).save()

        return super(ScheduleView, self).form_valid(form)


