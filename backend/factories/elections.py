import operator

import factory.fuzzy

from apollo.elections.models import Election, Question, Vote, Answer
from apollo.elections.models.election import VoterAuthorizationRule
from factories.users import UserFactory


class ElectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Election

    title = factory.Faker("name")
    author = factory.SubFactory(UserFactory)
    state = factory.fuzzy.FuzzyChoice(
        choices=map(operator.itemgetter(0), Election.State.choices)
    )
    visibility = factory.fuzzy.FuzzyChoice(
        choices=map(operator.itemgetter(0), Election.Visibility.choices)
    )


class VoterAuthorizationRuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VoterAuthorizationRule

    election = factory.SubFactory(ElectionFactory)
    type = factory.fuzzy.FuzzyChoice(
        choices=map(operator.itemgetter(0), VoterAuthorizationRule.Type.choices)
    )
    value = factory.Faker("email")


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question
        exclude = ["state"]

    question = factory.Faker("text")
    election = factory.SubFactory(
        ElectionFactory, state=factory.SelfAttribute("..state")
    )
    state = factory.fuzzy.FuzzyChoice(
        choices=map(operator.itemgetter(0), Election.State.choices)
    )


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    text = factory.Faker("text")
    question = factory.SubFactory(QuestionFactory)


class VoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vote

    answer = factory.SubFactory(AnswerFactory)
    answer_ciphertext = factory.Faker("pystr")
    author = factory.SubFactory(UserFactory)
    question = factory.SubFactory(QuestionFactory)
