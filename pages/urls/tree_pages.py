from django.urls import path
from pages.views import TreePageDetailView

#pretty lousy way to get things done :)

app_name = 'docs'
urlpatterns = [
    path('<slug>/', TreePageDetailView.as_view(), name = 'page_detail'),
    path('<a>/<slug>/', TreePageDetailView.as_view(), name = 'page_detail'),
    path('<a>/<b>/<slug>/',
        TreePageDetailView.as_view(), name = 'page_detail'),
    path('<a>/<b>/<c>/<slug>/',
        TreePageDetailView.as_view(), name = 'page_detail'),
    path('<a>/<b>/<c>/<d>/<slug>/',
        TreePageDetailView.as_view(), name = 'page_detail'),
    path('<a>/<b>/<c>/<d>/<e>/<slug>/',
        TreePageDetailView.as_view(), name = 'page_detail'),
    ]
