from django import forms
from django.shortcuts import render
from django.db.models import Q
from pagine.models import (Event, Blog, EventUpgrade, UserUpload)

class ValidateForm(forms.Form):
    q = forms.CharField(max_length=100)

def search_results(request):
    success = False
    form = ValidateForm(request.GET)
    if form.is_valid():
        q = request.GET['q']
        uploads = UserUpload.objects.filter(body__icontains = q)
        up_list = uploads.values_list('event_id', flat = True)
        upgrades = EventUpgrade.objects.filter(Q(title__icontains=q)|
            Q(body__icontains=q)).values_list('event_id', flat = True)
        events = Event.objects.filter(Q(title__icontains=q)|
            Q(intro__icontains=q)|Q(body__icontains=q)|
            Q(chronicle__icontains=q)|Q(restricted__icontains=q)|
            Q(id__in = upgrades)|Q(id__in = up_list))
        if events:
            success = True
        up_list = uploads.values_list('post_id', flat = True)
        blogs = Blog.objects.filter(Q(title__icontains=q)|
            Q(intro__icontains=q)|Q(body__icontains=q)|Q(id__in = up_list))
        if blogs:
            success = True
        return render(request, 'search_results.html', {'search': q,
            'all_events': events, 'all_blogs': blogs, 'success': success})
    else:
        return render(request, 'search_results.html', {'success': success, })
