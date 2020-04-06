from pytest_factoryboy import register
import factories

register(factories.UserFactory)
register(factories.UserFactory, "other_user")

register(factories.ElectionFactory)
register(factories.QuestionFactory)
register(factories.AnswerFactory)
register(factories.VoteFactory)
