import factory

from apollo.elections.models import Election, Question
from factories.users import UserFactory


class ElectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Election

    title = factory.Faker("name")
    author = factory.SubFactory(UserFactory)


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    question = factory.Faker("text")
    election = factory.SubFactory(ElectionFactory)
