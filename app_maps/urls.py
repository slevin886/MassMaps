from django.urls import path
from . import views

app_name = 'app_maps'

urlpatterns = [
    path('', views.home, name='home')
]