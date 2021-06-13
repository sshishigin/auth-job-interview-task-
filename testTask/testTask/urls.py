from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter

from user_api.views import UserViewSet

router = SimpleRouter()
router.register('api/v1/users', UserViewSet, basename='api-users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-get-token', obtain_auth_token, name='auth-token'),
]

urlpatterns += router.urls
