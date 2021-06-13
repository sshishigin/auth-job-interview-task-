from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from user_api.permissions import IsOwner
from user_api.serializers import ReadOnlyUserSerializer, WriteOnlyUserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    # permission_classes = [IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadOnlyUserSerializer
        return WriteOnlyUserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsOwner()]
        if self.action in ['list', 'destroy']:
            return [IsAdminUser()]
        else:
            return [AllowAny()]
