from rest_framework import permissions

from core.constants import USER_TYPES


class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ContentPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            if (
                request.user.is_authenticated
                and request.user.user_type == USER_TYPES.editor
            ):
                return True
        return True
