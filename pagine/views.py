from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView,
    TemplateView)
from taggit.models import Tag
from streamblocks.models import HomeButton

from .forms import UserUploadForm
from .models import (UserUpload, Blog, HomePage, Institutional)

class HomeTemplateView(TemplateView):
    template_name = 'pagine/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['page'] = HomePage.objects.first()
        except:
            raise Http404("Non ci sono Home Page")
        context['posts'] = Blog.objects.all()[:6]
        actions = context['page'].action.from_json()
        for action in actions:
            context['actions'] = HomeButton.objects.filter(id__in = action['id'])[:3]
        return context

class TagMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        if 'categoria' in self.request.GET:
            context['tag_filter'] = self.request.GET['categoria']
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if 'categoria' in self.request.GET:
            qs = qs.filter(tags__name=self.request.GET['categoria'])
        return qs

class ListBlog(TagMixin, ListView):
    model = Blog
    ordering = ('-date', )
    context_object_name = 'posts'
    paginate_by = 12

class DetailBlog(DetailView):
    model = Blog
    context_object_name = 'post'
    slug_field = 'slug'

class UserUploadCreateView(LoginRequiredMixin, CreateView):
    model = UserUpload
    form_class = UserUploadForm

    def get_success_url(self):
        if 'event_id' in self.request.GET:
            evt = Event.objects.get(id=self.request.GET['event_id'])
            return evt.get_path() + '/#upload-anchor'
        elif 'post_id' in self.request.GET:
            pst = Blog.objects.get(id=self.request.GET['post_id'])
            return pst.get_path() + '/#upload-anchor'

    def form_valid(self, form):
        form.instance.user = self.request.user
        if 'post_id' in self.request.GET:
            form.instance.post = Blog.objects.get(id=self.request.GET['post_id'])
        return super().form_valid(form)

#this is used by different institutional pages depending on type
def get_page(context, type):
    page = get_object_or_404(Institutional, type=type)
    context['page'] = page
    return context

class PrivacyTemplateView(TemplateView):
    template_name = 'pagine/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_page(context, '3-PR')
        return context
