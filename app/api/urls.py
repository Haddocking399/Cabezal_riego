from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('sensors/', views.sensors),
    path('pump/', views.pump),
    path('fertilizers/', views.fertilizers),
    path('breakers/', views.breakers),
    path('valves/', views.valves),
]