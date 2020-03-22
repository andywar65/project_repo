from django.urls import path, re_path
from pages.views import (TreePageDetailView, TreePageListView,
    page_by_path)

#pretty lousy way to get things done :)

app_name = 'docs'
urlpatterns = [
    path('', TreePageListView.as_view(), name = 'page_list'),
    path('<slug>/', TreePageDetailView.as_view(), name = 'page_by_slug'),
    re_path(r'^((?:[\w\-]+/)*)$', page_by_path, name = 'page_by_path'),
    ]
