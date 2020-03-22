from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
from streamblocks.models import HomeButton

from blog.models import Article
from .models import ( HomePage, TreePage )

class HomeTemplateView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = HomePage.objects.first()
        if not context['page']:
            raise Http404("Non ci sono Home Page")
        context['posts'] = Article.objects.all()[:6]
        actions = context['page'].action.from_json()
        for action in actions:
            context['actions'] = HomeButton.objects.filter(id__in = action['id'])[:3]
        return context

#this is used by different pages depending on slug
def get_page_by_slug(context, klass, slug):
    page = get_object_or_404( klass, slug=slug)
    context['page'] = page
    return context

class PrivacyTemplateView(TemplateView):
    template_name = 'pages/tree_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_page_by_slug(context, TreePage, 'privacy')
        return context

class TreePageListView(ListView):
    model = TreePage
    context_object_name = 'pages'
    template_name = 'pages/tree_page_list.html'

class TreePageDetailView(DetailView):
    model = TreePage
    context_object_name = 'page'
    slug_field = 'slug'
    template_name = 'pages/tree_page.html'
