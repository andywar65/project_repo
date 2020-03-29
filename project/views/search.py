from django import forms
from django.shortcuts import render
from django.db.models import Q
from blog.models import Article, UserUpload
from pages.models import TreePage

class ValidateForm(forms.Form):
    q = forms.CharField(max_length=100)

def search_results(request):
    success = False
    form = ValidateForm(request.GET)
    if form.is_valid():
        q = request.GET['q']
        #prepare list of user uploads referenced by blog posts
        uploads = UserUpload.objects.filter(body__icontains = q)
        uploads = uploads.values_list('post_id', flat = True)
        blogs = Article.objects.filter(Q(title__icontains=q)|
            Q(intro__icontains=q)|Q(stream_rendered__icontains = q)|
            Q(id__in = uploads))
        if blogs:
            success = True
        #TreePage page content type
        pages = TreePage.objects.filter(Q(title__icontains=q)|
            Q(intro__icontains=q)|Q(stream_rendered__icontains = q))
        if pages:
            success = True
        return render(request, 'search_results.html', {'search': q,
            'all_blogs': blogs, 'pages': pages, 'success': success})
    else:
        return render(request, 'search_results.html', {'success': success, })
