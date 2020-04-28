from pytest_factoryboy import register
import factories
from apollo.elections.models import Election

register(factories.UserFactory)
register(factories.UserFactory, "other_user")

register(factories.ElectionFactory)
register(factories.ElectionFactory, "opened_election", state=Election.State.OPENED)
register(factories.ElectionFactory, "frozen_election", state=Election.State.FROZEN)


register(factories.QuestionFactory)
register(factories.AnswerFactory)
register(factories.VoteFactory)
