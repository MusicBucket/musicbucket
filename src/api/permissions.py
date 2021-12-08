from rest_framework import permissions


class APIPermission(permissions.BasePermission):
    """
    Permission class used by allowing to access the API.
    Checks for the group 'api' in the request.user
    """

    API_PERMISSION_GROUP = "api"

    def has_permission(self, request, view):
        user = request.user
        for user_group in user.groups.all():
            if user_group.name == self.API_PERMISSION_GROUP:
                return True
        return False
