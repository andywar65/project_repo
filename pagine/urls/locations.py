from django.urls import path
from pagine.views import ListLocation, DetailLocation

urlpatterns = [
    path('', ListLocation.as_view(), name='locations'),
    path('<slug>/', DetailLocation.as_view(), name='location'),
    ]
