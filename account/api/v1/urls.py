from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account.api.v1.views import AuthViewSet, LogoutApiView

router = routers.SimpleRouter()
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
                  path('login', ObtainAuthToken.as_view()),
                  path('logout', LogoutApiView.as_view()),
                  path('jwt/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + router.urls
