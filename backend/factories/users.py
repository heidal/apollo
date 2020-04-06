import factory
from apollo.users.models import User
from faker import Factory as FakerFactory

faker = FakerFactory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda x: faker.name())
    email = factory.Faker("email")
