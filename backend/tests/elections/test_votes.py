from pytest import mark
from pytest_lazyfixture import lazy_fixture
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

import apollo.elections.models.vote
from apollo.elections import models as el_models
from apollo.users.models import User
from tests.elections.conftest import VotePostData
from tests.elections.utils import _create_vote

pytestmark = mark.django_db


def test_create_vote(
    api_client: APIClient, vote_data: VotePostData, eligible_voter: User
) -> None:
    response = _create_vote(api_client, vote_data, eligible_voter)
    assert response.status_code == status.HTTP_201_CREATED
    vote = el_models.Vote.objects.get(id=response.data["id"])
    assert all(
        (
            vote.answer_ciphertext == vote_data["answer_ciphertext"],
            vote.author.id == eligible_voter.id,
            vote.question.id == vote_data["question"],
        )
    )


def test_create_vote_twice_on_the_same_question(
    api_client: APIClient, vote: el_models.Vote
) -> None:
    response = _create_vote(
        api_client,
        {"answer_ciphertext": "baby yoda", "question": vote.answer.question.id},
        vote.author,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_cannot_create_for_non_existent_question(
    api_client: APIClient, vote_data: VotePostData, user: User
) -> None:
    vote_data["question"] = 4040
    response = _create_vote(api_client, vote_data, user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@mark.parametrize("param", ["answer_ciphertext", "question"])
def test_cannot_be_created_without_all_required_params(
    api_client: APIClient, param: str, vote_data: VotePostData, user: User
) -> None:
    del vote_data[param]
    response = _create_vote(api_client, vote_data, user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert param in str(response.data)


def test_cannot_be_created_without_logging_in(vote_data: VotePostData) -> None:
    api_client = APIClient()
    response = api_client.post(
        reverse("elections:vote-list"), data=vote_data, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_unauthorized_user_cannot_vote(
    api_client: APIClient, vote_data: VotePostData, user: User
) -> None:
    response = _create_vote(api_client, vote_data, user)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@mark.parametrize(
    "_question", [lazy_fixture("question"), lazy_fixture("question_in_closed_election")]
)
def test_cannot_vote_in_not_opened_election(
    api_client: APIClient,
    vote_data: VotePostData,
    user: User,
    eligible_voter_factory,
    _question: el_models.Question,
):
    voter = eligible_voter_factory(user=user, election=_question.election)
    vote_data["question"] = _question.id
    response = _create_vote(api_client, vote_data, voter)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_voter_is_created_on_first_vote(
    api_client: APIClient,
    vote_data: VotePostData,
    opened_election: el_models.Election,
    eligible_voter: User,
):
    response = _create_vote(api_client, vote_data, eligible_voter)
    assert response.status_code == status.HTTP_201_CREATED

    voter = apollo.elections.models.vote.Voter.objects.last()
    assert all((voter.user == eligible_voter, voter.election == opened_election))
