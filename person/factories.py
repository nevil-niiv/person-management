import factory
from datetime import date, datetime

from person.models import Person, Role


class RoleFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating Role instances for testing purposes.

    This factory generates Role objects with random values for
    `name` and `description` using the Faker library. It helps in
    automating the creation of Role instances in test cases.
    """

    name = factory.Faker("word")
    description = factory.Faker("sentence")

    class Meta:
        model = Role


class PersonFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating Person instances for testing purposes.

    This factory automates the creation of Person objects with realistic
    and randomized data using the Faker library. It also calculates the
    age based on the provided date of birth and hashes the password before
    saving the instance.
    """

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    date_of_birth = factory.Faker("date_of_birth")
    age = factory.LazyAttribute(lambda o: PersonFactory.calculate_age(
        o.date_of_birth))
    username = factory.Faker("user_name")
    password = factory.Faker("password")
    role = factory.SubFactory(RoleFactory)

    class Meta:
        model = Person

    @staticmethod
    def calculate_age(date_of_birth):
        """
        Calculate the age based on the given date of birth.

        Args:
            date_of_birth (datetime.date or str): The person's date of birth.

        Returns:
            int: The calculated age of the person.
        """
        today = date.today()
        date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d") \
            if isinstance(date_of_birth, str) else date_of_birth
        age = today.year - date_of_birth.year - (
                (today.month, today.day) <
                (date_of_birth.month, date_of_birth.day)
        )
        return age

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Custom creation method to set a hashed password before saving
        the instance.

        Args:
            model_class (type): The model class being created.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Person: A new Person instance with a hashed password.
        """
        obj = model_class(*args, **kwargs)
        obj.set_password(obj.password)
        obj.save()
        return obj
