from datetime import date, datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class TimestampMixin(models.Model):
    """
    Abstract model that provides timestamp fields
    for tracking creation and updates.

    Attributes:
        created_at (DateTimeField): Automatically stores the timestamp
            when the object is created.
        updated_at (DateTimeField): Automatically updates the timestamp
            when the object is modified.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Role(TimestampMixin):
    """
    Role model to define person roles (Admin or Guest).

    Attributes:
        name (CharField): The name of the role (e.g., "Admin", "Guest").
        description (TextField): Optional description of the role.
    """

    ADMIN = "admin"
    GUEST = "guest"

    ROLE_CHOICES = [
        (ADMIN, "Administrator"),
        (GUEST, "Guest"),
    ]

    name = models.CharField(
        _("role name"), max_length=50, choices=ROLE_CHOICES, unique=True
    )
    description = models.TextField(_("role description"),
                                   blank=True, null=True)

    def __str__(self):
        """
        Returns a string representation of the role.

        Returns:
            str: The name of the role.
        """
        return self.name


class Person(AbstractUser, TimestampMixin):
    """
    Custom user model extending Django's AbstractUser.

    - Adds additional fields specific to a person in the system.
    - Inherits built-in authentication-related fields such as
      first_name, last_name, username, email, and password.

    Attributes:
        phone_number (PhoneNumberField): Stores the person's
            phone number (optional).
        date_of_birth (DateField): Stores the person's
            date of birth (mandatory).
        age (IntegerField): Stores the calculated
            age of the person (optional, auto-calculated).

    Methods:
        calculate_age(): Calculates the person's age
            based on the date of birth.
        save(): Overrides the default save method
            to calculate and store age before saving.
        __str__(): Returns a string representation of the person.
    """

    phone_number = PhoneNumberField(_("phone number"), null=True, blank=True)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    age = models.IntegerField(_("age"), null=True, blank=True)

    # Assign role to a person (Each person belongs to one role)
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="person_role",
    )

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")

    def calculate_age(self):
        """
        Calculates the person's age based on their date of birth.

        Returns:
            int: The calculated age.
        """
        today = date.today()
        birth_date = self.date_of_birth
        age = (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )
        return age

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to ensure the age is calculated
        and stored before saving the instance.

        - If `age` is not provided, it calculates the age
          based on `date_of_birth`.
        - Ensures `date_of_birth` is properly formatted before saving.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """

        date_of_birth = self.date_of_birth
        if date_of_birth:
            self.date_of_birth = (
                datetime.strptime(date_of_birth, "%Y-%m-%d")
                if isinstance(date_of_birth, str)
                else date_of_birth
            )
            self.age = self.calculate_age()

        # Ensure the default role is assigned as Guest if no role is provided
        if not self.role:
            guest_role, created = Role.objects.get_or_create(
                name=Role.GUEST,
                defaults={"description": "Guest with limited access"}
            )
            self.role = guest_role
        return super(Person, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
