from rest_framework import viewsets, mixins, permissions

from account.api.v1.serializers import RegisterUserSerializer
from account.models import User


class UserRegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'create':
            return RegisterUserSerializer
