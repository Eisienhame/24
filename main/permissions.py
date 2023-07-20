from rest_framework import permissions
from rest_framework.permissions import BasePermission

from users.models import UserGroups


class ModeratorsPermissions(BasePermission):

    def has_permission(self, request, view):
        if (request.user.is_staff or (request.user.role == UserGroups.MODERATORS)) and request.method not in ['POST', 'DELETE']:
            return True
        return False


class UsersPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user or request.user.is_superuser:
            return True
        return False