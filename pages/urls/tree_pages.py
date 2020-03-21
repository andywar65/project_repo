from django.urls import path
from pages.views import *

app_name = 'docs'
urlpatterns = [
    path('<slug>/', TreePageDetailView.as_view(), name = 'page_detail'),
    ]
