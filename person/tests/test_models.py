from django.test import TestCase
from person.models import Role
from person.factories import PersonFactory, RoleFactory


class RoleModelTest(TestCase):
    """
    Test case for the Role model.

    This test suite verifies the creation and default behavior of
    Role instances. It ensures that roles can be created with
    specific names and descriptions and that a role always
    has a name.
    """

    def test_create_admin_role(self):
        """
        Test creating an admin role.

        This test ensures that a Role instance can be created with
        the name `ADMIN` and a specified description.
        """
        role = RoleFactory(name=Role.ADMIN, description="Administrator role")
        self.assertEqual(role.name, Role.ADMIN)
        self.assertEqual(role.description, "Administrator role")

    def test_create_guest_role(self):
        """
        Test creating a guest role.

        This test ensures that a Role instance can be created with
        the name `GUEST` and a specified description.
        """
        role = RoleFactory(name=Role.GUEST, description="Guest role")
        self.assertEqual(role.name, Role.GUEST)
        self.assertEqual(role.description, "Guest role")

    def test_role_default_name(self):
        """
        Test that a created role always has a name.

        This test ensures that when a Role instance is created using
        the factory withoutcspecifying a name, it still gets assigned
        a default valid name.
        """
        role = RoleFactory()
        self.assertIsNotNone(role.name)


class PersonModelTest(TestCase):
    """
    Test case for the Person model.

    This test suite verifies the creation of Person instances with
    different roles and ensures that key attributes such as name,
    phone number, role, and age are correctly set. It also tests
    string representation and age calculation functionality.
    """

    def test_create_admin_person(self):
        """
        Test creating an admin person.

        This test verifies that a Person instance with the ADMIN role
        can be created successfully, ensuring that the first name,
        phone number, and role are set correctly.
        """
        role = RoleFactory(name=Role.ADMIN, description="Administrator role")
        first_name = "Nevil"
        phone_number = "+44 20 7123 4567"
        person = PersonFactory(
            role=role, first_name=first_name, phone_number=phone_number
        )

        # Validate assigned attributes
        self.assertEqual(person.first_name, first_name)
        self.assertEqual(person.phone_number, phone_number)
        self.assertEqual(person.role.name, Role.ADMIN)

        # Ensure age is calculated correctly
        self.assertEqual(person.age, person.calculate_age())

    def test_create_guest_person(self):
        """
        Test creating a guest person.

        This test verifies that a Person instance with the GUEST role
        can be created successfully, ensuring that the first name,
        phone number, and role are set correctly.
        """
        role = RoleFactory(name=Role.GUEST, description="Guest role")
        first_name = "Guest"
        phone_number = "+44 20 7123 4567"
        person = PersonFactory(
            role=role, first_name=first_name, phone_number=phone_number
        )

        # Validate assigned attributes
        self.assertEqual(person.first_name, first_name)
        self.assertEqual(person.phone_number, phone_number)
        self.assertEqual(person.role.name, Role.GUEST)

        # Ensure age is calculated correctly
        self.assertEqual(person.age, person.calculate_age())

    def test_person_str_method(self):
        """
        Test the __str__ method of the Person model.

        This test ensures that the string representation of a Person
        instance correctly returns the full name in "First_Name Last_Name"
        format.
        """
        person = PersonFactory(first_name="Nevil", last_name="Kothari")
        self.assertEqual(str(person), "Nevil Kothari")

    def test_age_calculation(self):
        """
        Test the age calculation based on date_of_birth.

        This test verifies that the calculate_age method correctly computes
        the age of a Person based on their date of birth.
        """
        person = PersonFactory(date_of_birth="2000-01-01")

        # Assuming the current year is 2025, verify the calculated age
        self.assertEqual(person.calculate_age(), 25)
