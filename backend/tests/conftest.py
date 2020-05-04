from pytest import fixture
from pytest_factoryboy import register
from rest_framework.test import APIClient

import factories
from apollo.elections.models import Election

register(factories.UserFactory)
register(factories.UserFactory, "other_user")

register(factories.ElectionFactory, state=Election.State.CREATED)
register(factories.ElectionFactory, "opened_election", state=Election.State.OPENED)
register(factories.ElectionFactory, "frozen_election", state=Election.State.FROZEN)


register(factories.QuestionFactory)
register(factories.AnswerFactory)
register(factories.VoteFactory)


@fixture(scope="session")
def api_client():
    return APIClient()
