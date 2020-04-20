"""
API V1: Seller Permissions
"""
###
# Libraries
###

from rest_framework.permissions import BasePermission

###
# Permissions
###


class HasSeller(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and hasattr(request.user, 'seller'))
