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
    state=Election.State.OPENED,
    visibility=Election.Visibility.PUBLIC,
)
register(
    factories.ElectionFactory,
    "frozen_election",
    state=Election.State.CLOSED,
    visibility=Election.Visibility.PUBLIC,
)
register(
    factories.ElectionFactory,
    "private_election",
    visibility=Election.Visibility.PRIVATE,
)

register(factories.QuestionFactory)
register(factories.AnswerFactory)
register(factories.VoteFactory)

register(factories.VoterAuthorizationRuleFactory)


@fixture(scope="session")
def api_client():
    return APIClient()
