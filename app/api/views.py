from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Pump, Sensors, Fertilizers, Breakers, Valves
from .apps import daemon

def home(request):         
    return render(request, 'index.html', {
        'current': 'home',
        'title': 'Home',
        'ph': daemon.ph,
        'water_level': daemon.water_level,
        'pressure': daemon.pressure,
        'flow': daemon.flow,
        'salinity': daemon.salinity,
        'pump': daemon.pump,
        'breakers': daemon.breakers,
        'fertilizers': daemon.fertilizers,
        'valves': daemon.valves
    })

def pump(request):
    return render(request, 'pump.html', {
        'current': 'pump',
        'title': 'Bomba',
        'state': daemon.pump,
        'data': Pump.objects.all().order_by('date')[:60]
    })

def sensors(request):
    time = timezone.now() - timedelta(minutes=1)
    return render(request, 'sensors.html', {
        'current': 'sensors',
        'title': 'Sensores',
        'ph': daemon.ph,
        'water_level': daemon.water_level,
        'pressure': daemon.pressure,
        'flow': daemon.flow,
        'salinity': daemon.salinity,
        'data': Sensors.objects.filter(date__gte=time).order_by('date')
    })

def fertilizers(request):
    data = [
        Fertilizers.objects.filter(idx=0).order_by('date')[:60]
    ] 
    return render(request, 'fertilizers.html', {
        'current': 'fertilizers',
        'title': 'Fertilizantes'
    })

def breakers(request):
    return render(request, 'breakers.html', {
        'current': 'breakers',
        'title': 'Disyuntores'
    })

def valves(request):
    return render(request, 'valves.html', {
        'current': 'valves',
        'title': 'Válvulas'
    })