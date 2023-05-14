import factory
from .models import User
from faker import Factory

faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(
        lambda _: faker.profile(fields=["username"])["username"]
    )
    email = factory.LazyAttribute(lambda _: faker.email())
    first_name = faker.first_name()
    last_name = faker.last_name()
