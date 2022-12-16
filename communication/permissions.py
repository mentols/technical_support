from rest_framework.permissions import BasePermission


class IsOwnerOfTicket(BasePermission):
    """
    The request is authenticated as a user is the owner.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return bool(request.user and obj.author == request.user)


class CanChangeStatus(BasePermission):
    """
        The request is authenticated as a admin and put request method.
        """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return bool(request.method == 'PUT' and request.user.is_staff)
