from pytest import fixture
from pytest_factoryboy import register
from rest_framework.test import APIClient

import factories
from apollo.elections.models import Election

register(factories.UserFactory)
register(factories.UserFactory, "other_user")

register(
    factories.ElectionFactory,
    state=Election.State.CREATED,
    visibility=Election.Visibility.PUBLIC,
)
register(
    factories.ElectionFactory,
    "other_election",
    state=Election.State.CREATED,
    visibility=Election.Visibility.PUBLIC,
)
register(
    factories.ElectionFactory,
    "opened_election",
    open=True,
    visibility=Election.Visibility.PUBLIC,
)
register(
    factories.ElectionFactory,
    "closed_election",
    state=Election.State.CLOSED,
    visibility=Election.Visibility.PUBLIC,
)
register(
    factories.ElectionFactory,
    "private_election",
    visibility=Election.Visibility.PRIVATE,
)

register(factories.QuestionFactory)
register(factories.QuestionFactory, "question_in_opened_election")
register(factories.QuestionFactory, "question_in_closed_election")
register(factories.AnswerFactory)
register(factories.AnswerFactory, "answer_in_opened_election")

register(factories.VoteFactory)

register(factories.VoterAuthorizationRuleFactory)


@fixture(scope="session")
def api_client():
    return APIClient()


@fixture
def question_in_opened_election__election(opened_election):
    return opened_election


@fixture
def question_in_closed_election__election(closed_election):
    return closed_election


@fixture
def answer_in_opened_election__question(question_in_opened_election):
    return question_in_opened_election


@fixture
def election_with_votes(election, answer_factory, vote_factory):
    for i in range(3):
        answer_factory.create_batch(3, question__election=election)

    election.open()
