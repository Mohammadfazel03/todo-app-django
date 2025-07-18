from django.urls import path
from .views import CustomLoginView, CreateUserView, ChangePasswordView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('change_password/<str:token>/', ChangePasswordView.as_view(), name='change_password'),
]
