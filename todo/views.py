from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import generics

from .models import Task
from .serializers import TaskSerializer

class TaskTemplateView(TemplateView):
    template_name = 'todo/home.html'


class TaskUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ListTasksView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
