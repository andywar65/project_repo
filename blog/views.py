from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView,
    TemplateView)
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView,
    MonthArchiveView, DayArchiveView, )
from taggit.models import Tag

from .forms import UserUploadForm
from .models import (UserUpload, Article,)

class TagMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        if 'tag' in self.request.GET:
            context['tag_filter'] = self.request.GET['tag']
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if 'tag' in self.request.GET:
            qs = qs.filter(tags__name=self.request.GET['tag'])
        return qs

class ArticleArchiveIndexView(TagMixin, ArchiveIndexView):
    model = Article
    date_field = 'date'
    allow_future = True
    context_object_name = 'posts'
    paginate_by = 12
    allow_empty = True

class ArticleYearArchiveView(TagMixin, YearArchiveView):
    model = Article
    make_object_list = True
    date_field = 'date'
    allow_future = True
    context_object_name = 'posts'
    paginate_by = 12
    year_format = '%Y'
    allow_empty = True

class ArticleMonthArchiveView(TagMixin, MonthArchiveView):
    model = Article
    date_field = 'date'
    allow_future = True
    context_object_name = 'posts'
    year_format = '%Y'
    month_format = '%m'
    allow_empty = True

class ArticleDayArchiveView(TagMixin, DayArchiveView):
    model = Article
    date_field = 'date'
    allow_future = True
    context_object_name = 'posts'
    year_format = '%Y'
    month_format = '%m'
    day_format = '%d'
    allow_empty = True

class DetailArticle(DetailView):
    model = Article
    context_object_name = 'post'
    slug_field = 'slug'

class UserUploadCreateView(LoginRequiredMixin, CreateView):
    model = UserUpload
    form_class = UserUploadForm

    def get_success_url(self):
        if 'post_id' in self.request.GET:
            pst = Article.objects.get(id=self.request.GET['post_id'])
            return pst.get_path() + '/#upload-anchor'
        return super(UserUploadCreateView, self).get_success_url(self)

    def form_valid(self, form):
        form.instance.user = self.request.user
        if 'post_id' in self.request.GET:
            form.instance.post = Article.objects.get(id=self.request.GET['post_id'])
        return super().form_valid(form)
