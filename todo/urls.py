from django.urls import path

from .views import TaskTemplateView, TaskUpdateView, ListTasksView, TaskDeleteView

urlpatterns = [
    path('', TaskTemplateView.as_view(), name='home'),
    path('api/<int:pk>/', TaskUpdateView.as_view(), name='update-task'),
    path('api/<int:pk>/delete/', TaskDeleteView.as_view(), name='delete-task'),
    path('api/', ListTasksView.as_view(), name='list-task'),
]
