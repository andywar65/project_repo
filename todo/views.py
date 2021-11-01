from django.shortcuts import render
from rest_framework import generics

from .models import Task
from .serializers import TaskSerializer


def home_view(request):
    return render(request, 'todo/home.html', {})


class TaskUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ListTasksView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
