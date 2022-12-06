from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOfTicket(BasePermission):
    """
    The request is authenticated as a user is the owner.
    """

    def has_object_permission(self, request, view, obj):
        print("FFFF")
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and obj.author == request.user
        )
