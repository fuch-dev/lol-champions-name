# champions/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # La URL raíz de la app mostrará la lista de campeones
    path('', views.champion_list, name='champion_list'),
]