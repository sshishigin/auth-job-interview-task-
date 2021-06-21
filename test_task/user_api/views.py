from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet

from user_api.permissions import IsOwner
from user_api.serializers import ReadOnlyUserSerializer, WriteOnlyUserSerializer


class UserViewSet(ModelViewSet):
    # решил для скорости использовать modelviewset (пришлось попотеть над permissions)
    queryset = User.objects.all()
    # permission_classes = [IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly]
    # переопределил получение сериалайзера модели в зависимости от метода

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadOnlyUserSerializer
        return WriteOnlyUserSerializer

    # в зависимости от метода запроса требую разные permissions
    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsOwner()]
        if self.action in ['list', 'destroy']:
            return [IsAdminUser()]
        else:
            return [AllowAny()]
