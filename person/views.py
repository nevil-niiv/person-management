from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from person.models import Person
from person.pagination import PersonPagination, paginate
from person.permissions import IsAdmin, IsAdminOrGuest
from person.serializers import PersonSerializer, LoginSerializer

from django.contrib.auth import login, authenticate, logout

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class LoginAPIView(GenericAPIView):
    """
    API view to handle person login.

    - Accepts `username` and `password` in a POST request.
    - Authenticates the person against the database.
    - Logs in the person upon successful authentication.
    - Returns appropriate error messages for invalid or inactive person.

    Permissions:
    - Open to all people (no authentication required).
    - Does not enforce permissions as login itself is an entry point.

    Methods:
        post(request):
            Logs out the authenticated person and clears the session.
    """

    serializer_class = LoginSerializer
    authentication_classes = []  # No authentication required for login
    permission_classes = []  # No permissions required for login
    allowed_methods = ["post"]  # Only POST method is allowed

    def post(self, request):
        """
        Handles person login.

        Request Body:
            - username (str): The person's username.
            - password (str): The person's password.

        Response:
            - 200 OK: If login is successful.
            - 400 Bad Request: If credentials are incorrect or
              the person is inactive.

        Returns:
            - Success message if login is successful.
            - Error message if login fails due to
              invalid credentials or inactive status.
        """

        # Deserialize and validate input data
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Authenticate person using provided credentials
            person = authenticate(
                self.request,
                username=data.get("username"),
                password=data.get("password"),
            )
            if person is None:
                return Response(
                    {"error": "Invalid Credentials"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if person is active
            if not person.is_active:
                return Response(
                    {"error": "Inactive Person"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Log in the authenticated person
            login(request, person)
            return Response(
                {"message": "Successfully logged in"},
                status=status.HTTP_200_OK
            )

        # Return validation errors
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(GenericAPIView):
    """
    API endpoint to log out a person.

    Permissions:
    - Only authenticated person can perform this.

    Methods:
        post(request):
            Logs out the authenticated person and clears the session.
    """

    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ["post"]  # Only POST method is allowed

    def post(self, request):
        """
        Handles person logout.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A success message upon logout.
        """
        logout(request)
        return Response(
            {"message": "Successfully logged out"},
            status=status.HTTP_200_OK
        )


class PersonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Person entities in the system.

    - Only Admin person can perform CRUD operations.
    - Implements pagination for the list of people.
    - Provides an extra endpoint to filter people based on
      first name, last name, or age.
    """

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAdmin]
    pagination_class = PersonPagination

    @paginate(exclude_fields=["username"])
    @action(
        detail=False,
        methods=["get"],
        url_path="filter-people",
        permission_classes=[IsAdminOrGuest],
    )
    def filter_people(self, request):
        """
        Custom endpoint to filter people by first name, last name, or age.

        Query Parameters:
            - first_name (str, optional): Filters by first name
              (case-insensitive, partial match).
            - last_name (str, optional): Filters by last name
              (case-insensitive, partial match).
            - age (int, optional): Filters by exact age.

        Permissions:
            - Both Admin and Guest people can access this endpoint.
            - Excludes sensitive fields like `username` from the response.

        Returns:
            - A filtered list of people based on the provided query parameters.
        """

        # Retrieve query parameters
        first_name = request.query_params.get("first_name", "")
        last_name = request.query_params.get("last_name", "")
        age = request.query_params.get("age", None)

        # Initialize empty query filter
        filter_people_query = Q()

        # Apply filters if provided
        if first_name:
            filter_people_query &= Q(first_name__icontains=first_name)
        if last_name:
            filter_people_query &= Q(last_name__icontains=last_name)
        if age:
            filter_people_query |= Q(age=age)

        # Fetch filtered people
        people_qs = self.queryset.filter(filter_people_query)
        return people_qs
