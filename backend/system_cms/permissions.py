from rest_framework import permissions


class IsStaffPermission(permissions.BasePermission):
    """
    Custom permission to only allow access to staff users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
