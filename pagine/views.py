from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView,
    TemplateView)
from taggit.models import Tag
from streamblocks.models import HomeButton

from blog.models import Article
from .models import ( HomePage, Institutional)

class HomeTemplateView(TemplateView):
    template_name = 'pagine/home.html'

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

#this is used by different institutional pages depending on slug
def get_page_by_slug(context, slug):
    page = get_object_or_404(Institutional, slug=slug)
    context['page'] = page
    return context

class PrivacyTemplateView(TemplateView):
    template_name = 'pagine/institutional_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_page_by_slug(context, 'privacy')
        return context
