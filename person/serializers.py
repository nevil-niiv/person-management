from rest_framework import serializers
from person.models import Person


class LoginSerializer(serializers.Serializer):
    """
    Serializer for person login data.

    - Validates the `username` and `password` fields
      that are required for authentication.
    - This serializer is used to deserialize
      incoming login data in the login view.

    Fields:
        - username: The person's username (required).
        - password: The person's password (required).
    """

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        fields = ("username", "password")


class PersonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Person model, used to convert Person instances to JSON
    and vice versa.

    - Includes standard fields like first_name, last_name, email, etc.
    - Password is marked as `write_only` to ensure
      it is not included in the response.
    - Custom initialization allows for dynamic exclusion of
      specified fields from the serialization.

    Fields:
        - id: Auto-generated primary key.
        - first_name: Person's first name.
        - last_name: Person's last name.
        - email: Person's email address.
        - phone_number: Person's phone number.
        - date_of_birth: Person's birth date.
        - age: Calculated dynamically based on the date of birth.
        - username: Unique identifier for login.
        - password: Used for person authentication (write-only).
    """

    class Meta:
        model = Person
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "date_of_birth",
            "age",
            "username",
            "password",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True
            }  # Password should not be included in the response
        }

    def __init__(self, *args, **kwargs):
        """
        Initializes the serializer with an option
        to exclude specific fields dynamically.

        If the `exclude_fields` keyword argument is provided, those fields will
        be removed from the serializer fields.

        Args:
            *args: Variable length argument list.
            **kwargs: Keyword arguments, including
                `exclude_fields` (list of field names to exclude).
        """

        # Extract `exclude_fields` from the keyword arguments (if provided)
        exclude_fields = kwargs.pop("exclude_fields", [])
        super().__init__(*args, **kwargs)

        # Remove the specified fields from the serializer, if any
        if exclude_fields:
            for field_name in exclude_fields:
                self.fields.pop(field_name, None)
