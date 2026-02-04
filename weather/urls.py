from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_view, name='weather'),
    path('about/', views.about_view, name='about'),
]