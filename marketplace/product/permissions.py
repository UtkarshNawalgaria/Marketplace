from rest_framework import permissions


class IsStoreStaffAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        request_user = request.user

        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request_user.is_authenticated and request_user.is_staff)
