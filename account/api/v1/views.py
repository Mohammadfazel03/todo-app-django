from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from account.api.v1.serializers import RegisterUserSerializer, UserEmailVerificationSerializer, PasswordSerializer
from account.models import User


class AuthViewSet(viewsets.ViewSet):

    def send_verify_email(self, user, request):
        current_site = get_current_site(request)
        token = AccessToken()
        token.set_exp(from_time=timezone.now())
        access_token = token.for_user(user)
        message = render_to_string('active_email.html', {
            'username': user.email, 'domain': current_site.domain,
            'token': str(access_token)
        })
        mail_subject = 'Activate your account.'
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()

    def send_reset_password_email(self, user, request):
        current_site = get_current_site(request)
        token = AccessToken()
        token.set_exp(from_time=timezone.now())
        access_token = token.for_user(user)
        message = render_to_string('reset_password_email.html', {
            'username': user.email,
            'domain': current_site.domain,
            'token': access_token
        })
        mail_subject = 'Activate your account.'
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()

    @extend_schema(
        request=RegisterUserSerializer,
        responses={
            201: RegisterUserSerializer
        }
    )
    @action(detail=False, methods=['post'], permission_classes=(permissions.AllowAny,))
    def register(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.send_verify_email(user, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=None,
        responses={
            200: None
        }
    )
    @action(detail=False, methods=['get'], url_path=r'veryfi/(?P<token>.+)', url_name='user-active',
            permission_classes=(permissions.AllowAny,))
    def verify(self, request, token, *args, **kwargs):
        try:
            token = AccessToken(token=token)
            user_id = token['user_id']
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return Response(data=None, status=status.HTTP_200_OK)
        except:
            raise AuthenticationFailed()

    @extend_schema(
        request=UserEmailVerificationSerializer,
        responses={
            200: None
        }
    )
    @action(detail=False, methods=['post'], url_path='resend_email_verify', permission_classes=(permissions.AllowAny,))
    def resend_verification_email(self, request, *args, **kwargs):
        serializer = UserEmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        self.send_verify_email(user, request)
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        request=UserEmailVerificationSerializer,
        responses={
            200: None
        }
    )
    @action(detail=False, methods=['post'])
    def reset_password(self, request, *args, **kwargs):
        serializer = UserEmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        self.send_reset_password_email(user, request)
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        request=PasswordSerializer,
        responses={
            200: None
        }
    )
    @action(detail=False, methods=['post'], url_path='change_password/(?P<token>.+)')
    def change_password(self, request, token, *args, **kwargs):
        try:
            token = AccessToken(token=token)
            user_id = token['user_id']
            user = User.objects.get(id=user_id)
        except:
            raise AuthenticationFailed()
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.password = make_password(serializer.validated_data['password'])
        user.save()
        return Response(data=None, status=status.HTTP_200_OK)


class LogoutApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        Token.objects.get(user=self.request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
