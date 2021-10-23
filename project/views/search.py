from django import forms
from django.shortcuts import render
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from blog.models import Article, UserUpload
from portfolio.models import Project
from buildings.models import Journal
from pages.models import TreePage

class ValidateForm(forms.Form):
    q = forms.CharField(max_length=100)

def search_results(request):
    success = False
    form = ValidateForm(request.GET)
    if form.is_valid():
        q = SearchQuery(request.GET['q'])
        #search in uploads
        v = SearchVector('body')
        uploads = UserUpload.objects.annotate(rank=SearchRank(v, q))
        uploads = uploads.filter(rank__gt=0.01).values_list('post_id',
            flat = True)
        article_uploads = Article.objects.filter(uuid__in = uploads)
        if article_uploads:
            success = True
        #search in articles
        v = SearchVector('title', 'intro', 'body')
        articles = Article.objects.annotate(rank=SearchRank(v, q))
        articles = articles.filter(rank__gt=0.01)
        if articles:
            articles = articles.order_by('-rank')
            success = True
        #search in pages
        pages = TreePage.objects.annotate(rank=SearchRank(v, q))
        pages = pages.filter(rank__gt=0.01)
        if pages:
            pages = pages.order_by('-rank')
            success = True
        #search in projects
        progs = Project.objects.annotate(rank=SearchRank(v, q))
        progs = progs.filter(rank__gt=0.01)
        if progs:
            progs = progs.order_by('-rank')
            success = True
        #search in journals
        jours = Journal.objects.annotate(rank=SearchRank(v, q))
        jours = jours.filter(rank__gt=0.01)
        if jours:
            jours = jours.order_by('-rank')
            success = True

        return render(request, 'search_results.html',
            {'search': request.GET['q'], 'all_uploads': article_uploads,
            'all_blogs': articles, 'pages': pages, 'progs': progs,
            'jours': jours,
            'success': success})
    else:
        return render(request, 'search_results.html', {'success': success, })
