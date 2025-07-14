from rest_framework import routers

from task.api.v1.views import TaskViewSet

router = routers.SimpleRouter()
router.register(r'task', TaskViewSet, 'tasks')
urlpatterns = [] + router.urls
