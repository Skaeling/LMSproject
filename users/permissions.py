from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Возвращает True, если пользователь является модератором"""
    message = "Adding lms-objects not allowed"

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moders').exists()


class IsOwner(permissions.BasePermission):
    """Возвращает True, если пользователь является владельцем объекта"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
