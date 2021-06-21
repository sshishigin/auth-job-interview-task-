from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    #кастомная модель Permission которая позволяет совершать действия только со своими данными аккаунта
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
