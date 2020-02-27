from django.urls import path
from pagine.views import ListBlog, DetailBlog, UserUploadCreateView

app_name = 'blog'
urlpatterns = [
    path('contributi/', UserUploadCreateView.as_view(),
        name = 'post_upload'),
    path('', ListBlog.as_view(), name='posts'),
    path('<slug>/', DetailBlog.as_view(), name='post'),
    ]
