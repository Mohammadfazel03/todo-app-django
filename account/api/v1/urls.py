from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken

from account.api.v1.views import UserRegisterViewSet, LogoutApiView

router = routers.SimpleRouter()
router.register(r'register', UserRegisterViewSet)

urlpatterns = [
                  path('login', ObtainAuthToken.as_view()),
                  path('logout', LogoutApiView.as_view()),
              ] + router.urls
