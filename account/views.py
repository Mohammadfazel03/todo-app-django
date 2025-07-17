from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from rest_framework_simplejwt.tokens import AccessToken

from account.forms import EmailAuthenticationForm, CreateUserForm, ChangePasswordForm
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


class ChangePasswordView(FormView):
    form_class = ChangePasswordForm
    template_name = 'reset_password.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if "token" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'token' parameters."
            )

        token = kwargs.pop('token')

        try:
            token = AccessToken(token=token)
            user_id = token['user_id']
            self.user = User.objects.get(id=user_id)

        except:
            raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.user.password = make_password(form.cleaned_data['password2'])
        self.user.save()
        return super().form_valid(form)