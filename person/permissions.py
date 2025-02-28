from rest_framework import permissions
from person.models import Role


class IsAdmin(permissions.BasePermission):
    """
    Custom permission class to allow access only to the person
    with the 'Admin' role.

    Methods:
        has_permission(request, view):
            Checks if the person is authenticated and has the 'Admin' role.

    Usage:
        Apply this permission to views that should be
        restricted to admin people only.
    """

    def has_permission(self, request, view):
        """
        Determines whether the person has permission to access the view.

        Args:
            request (Request): The HTTP request object.
            view (View): The view being accessed.

        Returns:
            bool: True if the person is authenticated and
                has the 'Admin' role, False otherwise.
        """
        person = request.user
        if person.is_authenticated:
            person_role = person.role.name if person.role else Role.GUEST
            if person_role == Role.ADMIN:
                return True
        return False


class IsAdminOrGuest(permissions.BasePermission):
    """
    Custom permission class to allow access to people with
    either 'Admin' or 'Guest' roles.

    Methods:
        has_permission(request, view):
            Checks if the person is authenticated and has
            either the 'Admin' or 'Guest' role.

    Usage:
        Apply this permission to views that should be
        accessible to both admin and guest people.
    """

    def has_permission(self, request, view):
        """
        Determine whether the person has permission to access the view.

        Args:
            request (Request): The HTTP request object.
            view (View): The view being accessed.

        Returns:
            bool: True if the person is authenticated and has
                the 'Admin' or 'Guest' role, False otherwise.
        """
        person = request.user
        if person.is_authenticated:
            person_role = person.role.name if person.role else Role.GUEST
            if person_role in [Role.ADMIN, Role.GUEST]:
                return True
        return False
