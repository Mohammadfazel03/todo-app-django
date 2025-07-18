from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.password_validation import get_default_password_validators, validate_password
from django.utils.translation import gettext_lazy as _

from account.models import User


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'})
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(
        required=True,
        label=_("Password"),
    )
    password2 = forms.CharField(
        required=True,
        label=_("Password confirmation"),
    )
    captcha = CaptchaField()

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data['password2']

    def clean(self):
        validators = get_default_password_validators()
        validate_password(password=self.cleaned_data['password2'], password_validators=validators)
        return self.cleaned_data
