from pytest_factoryboy import register
from factories import UserFactory, ElectionFactory, QuestionFactory

register(UserFactory)
register(UserFactory, "other_user")

register(ElectionFactory)
register(QuestionFactory)
