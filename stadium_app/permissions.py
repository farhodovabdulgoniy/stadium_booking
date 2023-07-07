from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Admin'
    

class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Owner' or request.user.role == 'Admin'


class IsUserOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'User' or request.user.role == 'Admin'