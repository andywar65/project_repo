from django.urls import path
from blog.views import (ArticleArchiveIndexView, ArticleYearArchiveView,
    ArticleMonthArchiveView, ArticleDayArchiveView, DetailArticle,
    UserUploadCreateView, AuthorListView, ByAuthorListView)

app_name = 'blog'
urlpatterns = [
    path('', ArticleArchiveIndexView.as_view(), name = 'post_index'),
    path('<int:year>/', ArticleYearArchiveView.as_view(),
        name = 'post_year'),
    path('<int:year>/<int:month>/', ArticleMonthArchiveView.as_view(),
        name = 'post_month'),
    path('<int:year>/<int:month>/<int:day>/', ArticleDayArchiveView.as_view(),
        name = 'post_day'),
    path('<int:year>/<int:month>/<int:day>/<slug>/', DetailArticle.as_view(),
        name = 'post_detail'),
    path('contributi/', UserUploadCreateView.as_view(),
        name = 'post_upload'),
    path('autori/', AuthorListView.as_view(),
        name = 'article_authors'),
    path('autori/<int:pk>/', ByAuthorListView.as_view(),
        name = 'articles_by_author'),
    ]
