from rest_framework import routers

from account.api.v1.views import UserRegisterViewSet

router = routers.SimpleRouter()
router.register(r'register', UserRegisterViewSet)

urlpatterns = [] + router.urls
