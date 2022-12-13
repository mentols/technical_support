from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOfTicket(BasePermission):
    """
    The request is authenticated as a user is the owner.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return bool(request.user and obj.author == request.user)
