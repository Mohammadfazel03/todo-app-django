from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from account.forms import EmailAuthenticationForm

class CustomLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'login.html'
    next_page = reverse_lazy('task:index')
    redirect_authenticated_user = True

