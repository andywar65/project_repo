from django import forms
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.db.models import Q
from blog.models import Article, UserUpload
from pagine.models import Institutional

class ValidateForm(forms.Form):
    q = forms.CharField(max_length=100)

def search_results(request):
    success = False
    form = ValidateForm(request.GET)
    if form.is_valid():
        q = request.GET['q']
        #prepare list of indexed paragraphs containing query
        paragraphs = IndexedParagraph.objects.filter(Q(body__icontains = q)|
            Q(title__icontains = q))
        #blog content type
        bl_type = ContentType.objects.get(app_label='blog', model='article').id
        #filter paragraphs by blog type
        bl_paragraphs = paragraphs.filter( parent_type = bl_type )
        #extract list of blogs
        bl_list = bl_paragraphs.values_list('parent_id', flat = True)
        #prepare list of user uploads referenced by blog posts
        up_list = uploads.values_list('post_id', flat = True)
        blogs = Article.objects.filter(Q(title__icontains=q)|
            Q(intro__icontains=q)|Q(id__in = up_list)|Q(id__in = bl_list))
        if blogs:
            success = True
        #institutional page content type
        in_type = ContentType.objects.get(app_label='pagine', model='institutional').id
        #filter paragraphs by blog type
        in_paragraphs = paragraphs.filter( parent_type = in_type )
        #extract list of institutional pages
        in_list = in_paragraphs.values_list('parent_id', flat = True)
        inst = Institutional.objects.filter(Q(title__icontains=q)|
            Q(intro__icontains=q)|Q(id__in = in_list))
        if inst:
            success = True
        return render(request, 'search_results.html', {'search': q,
            'all_blogs': blogs, 'pages': inst, 'success': success})
    else:
        return render(request, 'search_results.html', {'success': success, })
