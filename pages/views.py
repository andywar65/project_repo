from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _

from blog.models import Article
from .models import ( HomePage, GalleryImage, HomeButton, TreePage )

class HomeTemplateView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = HomePage.objects.first()
        if not context['page']:
            raise Http404(_("No Home Pages available"))
        #we add this context to feed the standard gallery
        context['main_gall_slug'] = get_random_string(7)
        context['title'] = context['page'].title
        #context for the page
        context['images'] = context['page'].home_image.all()
        context['actions'] = context['page'].home_button.all()[:3]
        context['posts'] = Article.objects.all()[:6]
        return context

class TreePageListView(ListView):
    model = TreePage
    context_object_name = 'annotated_lists'
    template_name = 'pages/tree_page_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['annotated_lists'] = []
        root_pages = TreePage.get_root_nodes()
        for root_page in root_pages:
            context['annotated_lists'].append(TreePage.get_annotated_list(parent=root_page))
        return context

class TreePageDetailView(DetailView):
    model = TreePage
    context_object_name = 'page'
    slug_field = 'slug'
    template_name = 'pages/tree_page.html'

    def get_context_data(self, **kwargs):
        if not self.object.get_path() == self.request.path:
            raise Http404(_("Request path is different from GET path"))
        context = super().get_context_data(**kwargs)
        context['adjacent'] = self.object.get_adjacent_pages()
        return context

#unable to use class based view!
def page_by_path(request, path):
    path_list = path.split('/')
    #last element may be trailing slash
    while not path_list.pop():
        last = path_list.pop()
    page = get_object_or_404( TreePage, slug = last )
    if not page.get_path() == request.path:
        raise Http404(_("Request path is different from GET path"))
    adjacent = page.get_adjacent_pages()
    return render(request, 'pages/tree_page.html', { 'page': page,
        'adjacent': adjacent, })
