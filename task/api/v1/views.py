import requests
from django.core.cache import cache
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import BooleanField
from rest_framework.response import Response
from rest_framework.views import APIView

from core.settings import WEATHER_API_KEY
from task.api.v1.permissions import OwnerPermission
from task.api.v1.serializers import TaskSerializer, TaskChangeStateSerializer
from task.models import Task


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, OwnerPermission)
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    @extend_schema(

        responses={
            200: None
        }
    )
    @action(methods=['post'], detail=False, url_path='change_state/(?P<pk>\d)',
            serializer_class=TaskChangeStateSerializer)
    def change_state(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, task)
        task.is_complete = request.data['is_complete']
        task.save()
        return Response(status=status.HTTP_200_OK)


class WeatherApiView(APIView):

    def get(self, request, *args, **kwargs):
        if cache.has_key('weather'):
            return Response(cache.get('weather'))

        try:
            response = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?lat=33.97979&lon=51.444865&appid={WEATHER_API_KEY}')

            if response.status_code == 200:
                cache.set('weather', response.json(), timeout=20 * 60)
                return Response(response.json(), status=status.HTTP_200_OK)

            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
