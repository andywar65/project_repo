from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView,
    TemplateView)
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView,
    MonthArchiveView, DayArchiveView, )
from taggit.models import Tag

from .forms import UserUploadForm
from .models import (Location, Event, UserUpload, Blog)

class HomeTemplateView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_events'] = Event.objects.all()[:6]
        context['posts'] = Blog.objects.all()[:6]
        return context

class ListLocation(ListView):
    model = Location
    context_object_name = 'all_locations'
    paginate_by = 12

class DetailLocation(DetailView):
    model = Location
    context_object_name = 'location'
    slug_field = 'slug'

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

class EventArchiveIndexView(TagMixin, ArchiveIndexView):
    model = Event
    date_field = 'date'
    allow_future = True
    context_object_name = 'all_events'
    paginate_by = 12
    allow_empty = True

class EventYearArchiveView(TagMixin, YearArchiveView):
    model = Event
    make_object_list = True
    date_field = 'date'
    allow_future = True
    context_object_name = 'all_events'
    paginate_by = 12
    year_format = '%Y'
    allow_empty = True

class EventMonthArchiveView(TagMixin, MonthArchiveView):
    model = Event
    date_field = 'date'
    allow_future = True
    context_object_name = 'all_events'
    year_format = '%Y'
    month_format = '%m'
    allow_empty = True

class EventDayArchiveView(TagMixin, DayArchiveView):
    model = Event
    date_field = 'date'
    allow_future = True
    context_object_name = 'all_events'
    year_format = '%Y'
    month_format = '%m'
    day_format = '%d'
    allow_empty = True

class DetailEvent(DetailView):
    model = Event
    context_object_name = 'event'
    slug_field = 'slug'

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
        if 'event_id' in self.request.GET:
            form.instance.event = Event.objects.get(id=self.request.GET['event_id'])
        elif 'post_id' in self.request.GET:
            form.instance.post = Blog.objects.get(id=self.request.GET['post_id'])
        return super().form_valid(form)
