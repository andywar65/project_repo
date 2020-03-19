from django.urls import path
from pagine.views import (BlogArchiveIndexView, BlogYearArchiveView,
    BlogMonthArchiveView, BlogDayArchiveView, DetailBlog, UserUploadCreateView)

app_name = 'blog'
urlpatterns = [
    path('', BlogArchiveIndexView.as_view(), name = 'post_index'),
    path('<int:year>/', BlogYearArchiveView.as_view(),
        name = 'post_year'),
    path('<int:year>/<int:month>/', BlogMonthArchiveView.as_view(),
        name = 'post_month'),
    path('<int:year>/<int:month>/<int:day>/', BlogDayArchiveView.as_view(),
        name = 'post_day'),
    path('<int:year>/<int:month>/<int:day>/<slug>/', DetailBlog.as_view(),
        name = 'post_detail'),
    path('contributi/', UserUploadCreateView.as_view(),
        name = 'post_upload'),
    ]
