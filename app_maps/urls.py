from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'app_maps'

urlpatterns = [
    path('', views.home, name='home'),
    path('commutes/', views.CommuteList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
