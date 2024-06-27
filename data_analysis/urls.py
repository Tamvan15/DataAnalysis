# data_analysis/urls.py
from django.urls import path

from .views import analyze_data

urlpatterns = [
    path('', analyze_data, name='analyze_data'),
]
