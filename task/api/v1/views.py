from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import BooleanField
from rest_framework.response import Response

from task.api.v1.permissions import OwnerPermission
from task.api.v1.serializers import TaskSerializer
from task.models import Task


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, OwnerPermission)
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    @extend_schema(
        request=inline_serializer(
            'input',
            {
                'is_complete': BooleanField(required=True, allow_null=False),
            }
        ),
        responses={
            200: None
        }
    )
    @action(methods=['post'], detail=False, url_path='change_state/<int:pk>')
    def change_state(self, request, pk=None):
        if not request.data.get('is_complete') or request.data['is_complete'] not in [True, False]:
            raise ValidationError({'is_complete': "this fields is required"})

        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, task)
        task.is_complete = request.data['is_complete']
        task.save()
        return Response(status=status.HTTP_200_OK)
