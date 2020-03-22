from django import forms
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.db.models import Q
from blog.models import Article, UserUpload
from pages.models import TreePage
from streamblocks.models import IndexedParagraph

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
        uploads = UserUpload.objects.filter(body__icontains = q)
        up_list = uploads.values_list('post_id', flat = True)
        blogs = Article.objects.filter(Q(title__icontains=q)|
            Q(intro__icontains=q)|Q(id__in = up_list)|Q(id__in = bl_list))
        if blogs:
            success = True
        #TreePage page content type
        tp_type = ContentType.objects.get(app_label='pages', model='treepage').id
        #filter paragraphs by blog type
        tp_paragraphs = paragraphs.filter( parent_type = tp_type )
        #extract list of TreePage
        tp_list = tp_paragraphs.values_list('parent_id', flat = True)
        pages = TreePage.objects.filter(Q(title__icontains=q)|
            Q(intro__icontains=q)|Q(id__in = tp_list))
        if pages:
            success = True
        return render(request, 'search_results.html', {'search': q,
            'all_blogs': blogs, 'pages': pages, 'success': success})
    else:
        return render(request, 'search_results.html', {'success': success, })
