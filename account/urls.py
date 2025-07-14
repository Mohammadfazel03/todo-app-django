from django.urls import path
from .views import CustomLoginView, CreateUserView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CreateUserView.as_view(), name='register'),
]
