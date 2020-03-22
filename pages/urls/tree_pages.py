from django.urls import path
from pages.views import TreePageDetailView, TreePageListView

#pretty lousy way to get things done :)

app_name = 'docs'
urlpatterns = [
    path('', TreePageListView.as_view(), name = 'page_list'),
    path('<slug>/', TreePageDetailView.as_view(), name = 'page_detail_1'),
    path('<a>/<slug>/', TreePageDetailView.as_view(), name = 'page_detail_2'),
    path('<a>/<b>/<slug>/',
        TreePageDetailView.as_view(), name = 'page_detail_3'),
    path('<a>/<b>/<c>/<slug>/',
        TreePageDetailView.as_view(), name = 'page_detail_4'),
    path('<a>/<b>/<c>/<d>/<slug>/',
        TreePageDetailView.as_view(), name = 'page_detail_5'),
    path('<a>/<b>/<c>/<d>/<e>/<slug>/',
        TreePageDetailView.as_view(), name = 'page_detail_6'),
    ]
