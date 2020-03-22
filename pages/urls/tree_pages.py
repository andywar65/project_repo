from django.urls import path
from pages.views import TreePageDetailView

app_name = 'docs'
urlpatterns = [
    path('<slug>/', TreePageDetailView.as_view(), name = 'page_detail'),
    path('<a>/<slug>/', TreePageDetailView.as_view(), name = 'page_detail'),
    path('<a>/<b>/<slug>/', TreePageDetailView.as_view(), name = 'page_detail'),
    ]
