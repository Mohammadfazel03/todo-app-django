from django.urls import path
from rest_framework import routers

from task.api.v1.views import TaskViewSet, WeatherApiView

router = routers.SimpleRouter()
router.register(r'task', TaskViewSet, 'tasks')
urlpatterns = [
                  path('weather', WeatherApiView.as_view())
              ] + router.urls
