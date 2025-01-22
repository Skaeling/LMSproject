from rest_framework import permissions


class LMSAccessPermission(permissions.BasePermission):
    message = "Adding lms-objects not allowed"

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moders').exists()
