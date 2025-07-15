from rest_framework import viewsets, mixins, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from account.api.v1.serializers import RegisterUserSerializer
from account.models import User


class UserRegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'create':
            return RegisterUserSerializer


class LogoutApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        Token.objects.get(user=self.request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
