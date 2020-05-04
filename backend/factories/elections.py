import factory.fuzzy

from apollo.elections.models import Election, Question, Vote, Answer
from factories.users import UserFactory


class ElectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Election

    title = factory.Faker("name")
    author = factory.SubFactory(UserFactory)
    state = factory.fuzzy.FuzzyChoice(
        choices=map(lambda x: x[0], Election.State.choices)
    )


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    question = factory.Faker("text")
    election = factory.SubFactory(ElectionFactory)


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    text = factory.Faker("text")
    question = factory.SubFactory(QuestionFactory)


class VoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vote

    answer = factory.SubFactory(AnswerFactory)
    author = factory.SubFactory(UserFactory)
