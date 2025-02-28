from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from person.models import Role


class Command(BaseCommand):
    """
    Management command to create person with Admin and Guest roles.
    """

    help = "Creates Admin and Guest persons with predefined roles"

    def handle(self, *args, **kwargs):
        """
        The method executed when the command runs.
        It ensures that:
        - The 'Admin' and 'Guest' roles exist.
        - A person with each role is created if they don’t exist.
        """

        person_model = get_user_model()

        # Ensure Role objects exist
        admin_role, _ = Role.objects.get_or_create(
            name=Role.ADMIN,
            defaults={"description": "Administrator with full access"}
        )
        guest_role, _ = Role.objects.get_or_create(
            name=Role.GUEST,
            defaults={"description": "Guest with limited access"}
        )

        # Create Admin
        admin, is_admin_created = person_model.objects.get_or_create(
            username="admin",
            defaults={
                "first_name": "Admin",
                "last_name": "User",
                "email": "admin@example.com",
                "role": admin_role,
                "date_of_birth": "1995-09-01",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if is_admin_created:
            admin.set_password("admin123")  # Set password
            admin.save()
            self.stdout.write(
                self.style.SUCCESS("Successfully created Admin person.")
            )

        # Create Guest
        guest, is_guest_created = person_model.objects.get_or_create(
            username="guest",
            defaults={
                "first_name": "Guest",
                "last_name": "User",
                "email": "guest@example.com",
                "role": guest_role,
                "date_of_birth": "2015-01-01",
                "is_staff": False,
                "is_superuser": False,
            },
        )
        if is_guest_created:
            guest.set_password("guest123")  # Set password
            guest.save()
            self.stdout.write(
                self.style.SUCCESS("Successfully created Guest person.")
            )

        self.stdout.write(
            self.style.SUCCESS("Admin and Guest persons are "
                               "set up successfully.")
        )
