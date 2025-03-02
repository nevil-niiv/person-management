from rest_framework.test import APITestCase
from rest_framework import status
from person.models import Person, Role
from person.factories import PersonFactory, RoleFactory


class LoginAPITestCase(APITestCase):
    """
    Test case for the Login API endpoint.

    This test case covers:
    - Successful login with correct credentials.
    - Failed login attempts with incorrect credentials.
    """

    def setUp(self):
        """
        Set up test data before each test method.

        - Creates a test person using the PersonFactory.
        - Assigns the person the "Admin" role.
        - Sets and saves the password for authentication.
        - Defines the login API endpoint path.
        """
        self.person = PersonFactory(role=RoleFactory(name=Role.ADMIN))
        self.person.set_password("password123")
        self.person.save()
        self.login_path = "/api/login/"

    def test_login_success(self):
        """
        Test successful login with valid credentials.

        Expected outcome:
        - API should return 200 OK.
        - Response should contain a success message.
        """
        url = self.login_path
        data = {"username": self.person.username, "password": "password123"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Successfully logged in")

    def test_login_invalid_person(self):
        """
        Test login with incorrect credentials.

        Expected outcome:
        - API should return 400 Bad Request.
        - Response should contain an "error" key with an appropriate message.
        """
        url = self.login_path
        data = {"username": self.person.username, "password": "wrongpassword"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("error"), "Invalid Credentials")
        self.assertIn("error", response.data)


class LogoutAPITestCase(APITestCase):
    """
    Test case for the Logout API endpoint.

    This test case covers:
    - Successfully logging out an authenticated person.
    """

    def setUp(self):
        """
        Set up test data before each test method.

        - Creates a test person with the "Admin" role.
        - Sets and saves the password for authentication.
        - Defines the logout API endpoint path.
        """
        self.person = PersonFactory(role=RoleFactory(name=Role.ADMIN))
        self.person.set_password("password123")
        self.person.save()
        self.logout_path = "/api/logout/"

    def test_logout(self):
        """
        Test successful logout of an authenticated person.

        Steps:
        - Authenticate the test person using `force_authenticate`.
        - Send a POST request to the logout endpoint.
        - Validate the response status and message.

        Expected outcome:
        - API should return 200 OK.
        - Response should contain a success message.
        """
        self.client.force_authenticate(user=self.person)
        url = self.logout_path
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Successfully logged out")


class PersonAPITestCase(APITestCase):
    """
    Test case for Person API endpoints.

    This test class covers:
    - Listing people with different person roles.
    - Retrieving a specific person's details.
    - Filtering persons based on various attributes.
    - Creating, updating, and deleting persons with role-based access.
    """

    def setUp(self):
        """
        Set up test data before each test method.

        - Creates admin and guest roles.
        - Creates admin and guest persons with test credentials.
        - Defines passwords for authentication.
        """
        self.admin_role = RoleFactory(name=Role.ADMIN,
                                      description="Administrator role")
        self.guest_role = RoleFactory(name=Role.GUEST,
                                      description="Guest role")

        self.admin_person_password = "adminpassword"
        self.guest_person_password = "guestpassword"

        self.admin_person = PersonFactory(
            username="adminuser",
            email="admin@example.com",
            password=self.admin_person_password,
            role=self.admin_role,
            date_of_birth="2000-01-01",
        )

        self.guest_person = PersonFactory(
            username="guestuser",
            email="guest@example.com",
            password=self.guest_person_password,
            role=self.guest_role,
            date_of_birth="2010-01-01",
        )

        self.guest_person1 = PersonFactory(
            username="test_guest",
            email="test_guest@example.com",
            password=self.guest_person_password,
            role=self.guest_role,
            first_name="Python",
            last_name="Dev",
            date_of_birth="1995-09-01",
        )

    def authenticate_as_admin(self):
        """Helper method to authenticate as admin person."""
        admin_login = self.client.login(
            username="adminuser", password=self.admin_person_password
        )
        self.assertTrue(admin_login)

    def authenticate_as_guest(self):
        """Helper method to authenticate as guest person."""
        guest_login = self.client.login(
            username="guestuser", password=self.guest_person_password
        )
        self.assertTrue(guest_login)

    # ADMIN ROLE TEST CASES
    def test_person_list_by_admin(self):
        """
        Test listing all persons as an admin.

        Expected outcome:
        - API should return 200 OK.
        - Response should include person details excluding sensitive data.
        """
        self.authenticate_as_admin()
        url = "/api/person/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results")
        if results:
            result = results[0]
            self.assertIn("id", result)
            self.assertIn("first_name", result)
            self.assertIn("last_name", result)
            self.assertIn("email", result)
            self.assertIn("phone_number", result)
            self.assertIn("date_of_birth", result)
            self.assertIn("age", result)
            self.assertIn("username", result)
            self.assertNotIn("password", result)

    def test_retrieve_person_by_admin(self):
        """
        Test retrieving a person's details as an admin.

        Expected outcome:
        - API should return 200 OK.
        - Response should contain valid person details excluding password.
        """
        self.authenticate_as_admin()
        url = f"/api/person/{self.admin_person.id}/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data
        self.assertIn("id", result)
        self.assertIn("first_name", result)
        self.assertIn("last_name", result)
        self.assertIn("email", result)
        self.assertIn("phone_number", result)
        self.assertIn("date_of_birth", result)
        self.assertIn("age", result)
        self.assertIn("username", result)
        self.assertNotIn("password", result)

    def test_filter_people_by_first_name_by_admin(self):
        """
        Test filtering persons by first name as an admin.

        Expected outcome:
        - API should return 200 OK.
        - Response should only include people with the specified first name.
        """
        self.authenticate_as_admin()
        url = "/api/person/filter-people/?first_name=Python"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results")
        self.assertTrue(any(person["first_name"] == "Python"
                            for person in results))
        if results:
            result = results[0]
            self.assertIn("id", result)
            self.assertIn("first_name", result)
            self.assertIn("last_name", result)
            self.assertIn("email", result)
            self.assertIn("phone_number", result)
            self.assertIn("date_of_birth", result)
            self.assertIn("age", result)
            self.assertNotIn("username", result)
            self.assertNotIn("password", result)

    def test_filter_people_by_last_name_by_admin(self):
        """
        Test filtering persons by last name as an admin.

        Expected outcome:
        - API should return 200 OK.
        - Response should only include people with the specified last name.
        """
        self.authenticate_as_admin()
        url = "/api/person/filter-people/?last_name=Dev"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results")
        self.assertTrue(any(person["last_name"] == "Dev"
                            for person in results))
        if results:
            result = results[0]
            self.assertIn("id", result)
            self.assertIn("first_name", result)
            self.assertIn("last_name", result)
            self.assertIn("email", result)
            self.assertIn("phone_number", result)
            self.assertIn("date_of_birth", result)
            self.assertIn("age", result)
            self.assertNotIn("username", result)
            self.assertNotIn("password", result)

    def test_filter_people_by_age_by_admin(self):
        """
        Test filtering persons by age as an admin.

        Expected outcome:
        - API should return 200 OK.
        - Response should only include people with the specified age.
        """
        self.authenticate_as_admin()
        url = "/api/person/filter-people/?age=29"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results")
        self.assertTrue(any(person["age"] == 29 for person in results))
        if results:
            result = results[0]
            self.assertIn("id", result)
            self.assertIn("first_name", result)
            self.assertIn("last_name", result)
            self.assertIn("email", result)
            self.assertIn("phone_number", result)
            self.assertIn("date_of_birth", result)
            self.assertIn("age", result)
            self.assertNotIn("username", result)
            self.assertNotIn("password", result)

    def test_create_person_by_admin(self):
        """
        Test creating a new person as an admin.

        Expected outcome:
        - API should return 201 CREATED.
        - The new person should be successfully added.
        """
        self.authenticate_as_admin()
        url = "/api/person/"
        data = {
            "first_name": "Test",
            "last_name": "Person",
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123",
            "role": self.admin_role.id,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["first_name"], "Test")

    def test_update_person_by_admin(self):
        """
        Test updating a person's details as an admin.

        Expected outcome:
        - API should return 200 OK.
        - The updated details should be reflected in the response.
        """
        self.authenticate_as_admin()
        url = f"/api/person/{self.admin_person.id}/"
        data = {"first_name": "UpdatedName"}

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "UpdatedName")

    def test_delete_person_by_admin(self):
        """
        Test deleting a person as an admin.

        Expected outcome:
        - API should return 204 NO CONTENT.
        - The deleted person should no longer exist in the database.
        """
        self.authenticate_as_admin()
        url = f"/api/person/{self.admin_person.id}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertRaises(
            Person.DoesNotExist, Person.objects.get, id=self.admin_person.id
        )

    # GUEST ROLE TEST CASES
    def test_person_list_by_guest(self):
        """
        Test if a guest person can list persons.

        Expected outcome:
        - API should return 403 FORBIDDEN.
        """
        self.authenticate_as_guest()
        url = "/api/person/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_person_by_guest(self):
        """
        Test if a guest person can retrieve a person's details.

        Expected outcome:
        - API should return 403 FORBIDDEN.
        """
        self.authenticate_as_guest()
        url = f"/api/person/{self.guest_person.id}/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_people_by_first_name_by_guest(self):
        """
        Test filtering persons by first name as a guest.

        Expected outcome:
        - API should return 200 OK.
        - Response should only include people with the specified first name.
        """
        self.authenticate_as_guest()
        url = "/api/person/filter-people/?first_name=Python"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results")
        self.assertTrue(any(person["first_name"] == "Python"
                            for person in results))
        if results:
            result = results[0]
            self.assertIn("id", result)
            self.assertIn("first_name", result)
            self.assertIn("last_name", result)
            self.assertIn("email", result)
            self.assertIn("phone_number", result)
            self.assertIn("date_of_birth", result)
            self.assertIn("age", result)
            self.assertNotIn("username", result)
            self.assertNotIn("password", result)

    def test_filter_people_by_last_name_by_guest(self):
        """
        Test filtering persons by last name as a guest.

        Expected outcome:
        - API should return 200 OK.
        - Response should only include people with the specified last name.
        """
        self.authenticate_as_guest()
        url = "/api/person/filter-people/?last_name=Dev"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results")
        self.assertTrue(any(person["last_name"] == "Dev"
                            for person in results))
        if results:
            result = results[0]
            self.assertIn("id", result)
            self.assertIn("first_name", result)
            self.assertIn("last_name", result)
            self.assertIn("email", result)
            self.assertIn("phone_number", result)
            self.assertIn("date_of_birth", result)
            self.assertIn("age", result)
            self.assertNotIn("username", result)
            self.assertNotIn("password", result)

    def test_filter_people_by_age_by_guest(self):
        """
        Test filtering persons by age as a guest.

        Expected outcome:
        - API should return 200 OK.
        - Response should only include people with the specified age.
        """
        self.authenticate_as_guest()
        url = "/api/person/filter-people/?age=29"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results")
        self.assertTrue(any(person["age"] == 29 for person in results))
        if results:
            result = results[0]
            self.assertIn("id", result)
            self.assertIn("first_name", result)
            self.assertIn("last_name", result)
            self.assertIn("email", result)
            self.assertIn("phone_number", result)
            self.assertIn("date_of_birth", result)
            self.assertIn("age", result)
            self.assertNotIn("username", result)
            self.assertNotIn("password", result)

    def test_create_person_by_guest(self):
        """
        Test if a guest person can create a person.

        Expected outcome:
        - API should return 403 FORBIDDEN.
        """
        self.authenticate_as_guest()
        url = "/api/person/"
        data = {
            "first_name": "Test",
            "last_name": "Person",
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123",
            "role": self.guest_role.id,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_person_by_guest(self):
        """
        Test if a guest person can update a person.

        Expected outcome:
        - API should return 403 FORBIDDEN.
        """
        self.authenticate_as_guest()
        url = f"/api/person/{self.guest_person.id}/"
        data = {"first_name": "UpdatedGuestName"}

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_person_by_guest(self):
        """
        Test if a guest person can delete a person.

        Expected outcome:
        - API should return 403 FORBIDDEN.
        """
        self.authenticate_as_guest()
        url = f"/api/person/{self.guest_person.id}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
