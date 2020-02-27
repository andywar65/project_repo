from django.urls import path
from pagine.views import (EventArchiveIndexView, EventYearArchiveView,
    EventMonthArchiveView, EventDayArchiveView, DetailEvent, UserUploadCreateView )

app_name = 'pagine'

urlpatterns = [
    path('', EventArchiveIndexView.as_view(), name = 'event_index'),
    path('<int:year>/', EventYearArchiveView.as_view(),
        name = 'event_year'),
    path('<int:year>/<int:month>/', EventMonthArchiveView.as_view(),
        name = 'event_month'),
    path('<int:year>/<int:month>/<int:day>/', EventDayArchiveView.as_view(),
        name = 'event_day'),
    path('<int:year>/<int:month>/<int:day>/<slug>/', DetailEvent.as_view(),
        name = 'event_detail'),
    path('contributi/', UserUploadCreateView.as_view(),
        name = 'event_upload'),
    ]
