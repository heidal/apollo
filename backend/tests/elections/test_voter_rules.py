import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from rest_framework.test import APIClient

from apollo.users import models
from apollo.elections import models as el_models
from apollo.elections.models import Election
from tests.elections.conftest import VotePostData
from tests.elections.utils import _create_vote

pytestmark = pytest.mark.django_db


@pytest.fixture
def election_with_voters_rules(
    opened_election,
    answer_factory,
    question_factory,
    voter_authorization_rule_factory,
    user,
):
    election = opened_election
    questions = question_factory.create_batch(5, election=election)
    for question in questions:
        answer_factory.create_batch(3, question=question)

    voter_authorization_rule_factory(
        type=el_models.VoterAuthorizationRule.Type.EXACT, value=user, election=election
    )
    return election


def test_voter_authorized_in_one_election_cannot_vote_in_another(
    api_client: APIClient,
    eligible_voter: models.User,
    vote_data: VotePostData,
    question_factory,
):
    other_election_question = question_factory(state=el_models.Election.State.OPENED)
    vote_data["question"] = other_election_question.id
    response = _create_vote(api_client, vote_data, eligible_voter)
    assert response.status_code == status.HTTP_403_FORBIDDEN
