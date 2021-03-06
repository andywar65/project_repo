from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView,
    TemplateView)
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView,
    MonthArchiveView, DayArchiveView, )
from django.utils.crypto import get_random_string

from taggit.models import Tag

from users.models import User

from .forms import UserUploadForm
from .models import (UserUpload, Article,)
from .management.commands.fetch_article_emails import do_command

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

    def setup(self, request, *args, **kwargs):
        super(ArticleArchiveIndexView, self).setup(request, *args, **kwargs)
        do_command()

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #we add the following to feed standardized gallery
        context['main_gall_slug'] = get_random_string(7)
        context['title'] = self.object.title
        #gallery images
        context['images'] = self.object.article_image.all()

        return context

class UserUploadCreateView(PermissionRequiredMixin, CreateView):
    model = UserUpload
    form_class = UserUploadForm
    permission_required = 'blog.add_userupload'

    def get_success_url(self):
        if 'post_id' in self.request.GET:
            post = Article.objects.get(slug=self.request.GET['post_id'])
            return post.get_path() + '/#upload-anchor'
        return super(UserUploadCreateView, self).get_success_url(self)

    def form_valid(self, form):
        form.instance.user = self.request.user
        if 'post_id' in self.request.GET:
            form.instance.post = Article.objects.get(slug=self.request.GET['post_id'])
        return super(UserUploadCreateView, self).form_valid(form)

class AuthorListView(ListView):
    model = User
    #context_object_name = 'authors'
    template_name = 'blog/author_list.html'
    paginate_by = 10
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_users = context['user_list']
        all_articles = Article.objects.all()
        all_contrib = UserUpload.objects.all()
        author_dict = {}
        for author in all_users:
            art_count = all_articles.filter(author_id = author.uuid).count()
            contrib_count = all_contrib.filter(user_id = author.uuid).count()
            if art_count or contrib_count:
                author_dict[author]=(art_count, contrib_count)
        context['authors'] = author_dict
        return context

class ByAuthorListView(ListView):
    model = Article
    context_object_name = 'posts'
    template_name = 'blog/article_archive_authors.html'
    paginate_by = 12
    allow_empty = True

    """We cannot subclass TagMixin because queryset is altered (by author), so
    the TagMixin snippets are included in get_queryset() and get() afterwards"""

    def get_queryset(self):
        qs = Article.objects.filter(author__username= self.kwargs['username'])
        if 'tag' in self.request.GET:
            qs = qs.filter(tags__name=self.request.GET['tag'])
        return qs

    def get(self, request, *args, **kwargs):
        super(ByAuthorListView, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        context['author'] = get_object_or_404( User, username = kwargs['username'] )
        context['tags'] = Tag.objects.all()
        if 'tag' in self.request.GET:
            context['tag_filter'] = self.request.GET['tag']
        return self.render_to_response(context)

class ByUploadListView(ListView):
    model = UserUpload
    context_object_name = 'uploads'
    template_name = 'blog/uploads_by_author.html'
    paginate_by = 12
    allow_empty = True

    def get_queryset(self):
        qs = UserUpload.objects.filter(user_id__username= self.kwargs['username'])
        return qs

    def get(self, request, *args, **kwargs):
        super(ByUploadListView, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        context['author'] = get_object_or_404( User, username = kwargs['username'] )
        return self.render_to_response(context)
