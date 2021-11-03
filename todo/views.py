from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import generics

from .models import Task
from .serializers import TaskSerializer

class TaskTemplateView(TemplateView):
    template_name = 'todo/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perms'] = {
            'add': self.request.user.has_perm('todo.add_task'),
            'change': self.request.user.has_perm('todo.change_task'),
            'delete': self.request.user.has_perm('todo.delete_task'),
        }
        return context


class TaskUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ListTasksView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
