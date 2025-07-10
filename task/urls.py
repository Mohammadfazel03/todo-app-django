from django.contrib.auth import views as auth_views
from django.urls import path

from task.views import IndexView, CreateTaskView, UpdateTaskView, DeleteTaskView, ChangeStateTaskView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create', CreateTaskView.as_view(), name='create'),
    path('update/<int:pk>/', UpdateTaskView.as_view(), name='edit'),
    path('delete/<int:pk>/', DeleteTaskView.as_view(), name='delete'),
    path('change/state/<int:pk>/', ChangeStateTaskView.as_view(), name='change-state'),
]
