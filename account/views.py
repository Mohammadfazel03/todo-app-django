from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from account.forms import EmailAuthenticationForm, CreateUserForm
from account.models import User


class CustomLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'login.html'
    next_page = reverse_lazy('task:index')
    redirect_authenticated_user = True


class CreateUserView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'register.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('task:index'))
        return super().dispatch(request, *args, **kwargs)
