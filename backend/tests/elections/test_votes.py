from typing import TypedDict

from apollo.users.models import User
from pytest import mark, fixture
from unittest.mock import MagicMock
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from apollo.elections.models import Answer, Vote, Election

VotePostData = TypedDict("VotePostData", {"answer": int, "election": int})

pytestmark = mark.django_db


@fixture
def vote_data(answer: Answer) -> VotePostData:
    return {"answer": answer.id, "election": answer.question.election.id}


@fixture
def eligible_voter(
    user_factory, voter_authorization_rule_factory, election: Election
) -> User:
    user = user_factory()
    voter_authorization_rule_factory(election=election, value=user.email)
    return user


@fixture
def decrypt_mock(mocker, answer: Answer):
    mock = mocker.patch("apollo.elections.serializers.decrypt")
    mock.return_value = answer.id
    return mock


def _create_vote(
    api_client: APIClient, vote_data: VotePostData, user: User
) -> Response:
    api_client.force_authenticate(user=user)
    return api_client.post(
        reverse("elections:vote-list"), data=vote_data, format="json"
    )


def test_create_vote(
    api_client: APIClient,
    vote_data: VotePostData,
    eligible_voter: User,
    decrypt_mock: MagicMock,
) -> None:
    response = _create_vote(api_client, vote_data, eligible_voter)
    assert response.status_code == status.HTTP_201_CREATED
    vote = Vote.objects.get(id=response.data["id"])
    assert all(
        (vote.answer.id == vote_data["answer"], vote.author.id == eligible_voter.id)
    )


def test_create_vote_twice_on_the_same_thing(
    api_client: APIClient, vote: Vote, decrypt_mock: MagicMock
) -> None:
    response = _create_vote(
        api_client,
        {"answer": vote.answer.id, "election": vote.answer.question.election.id},
        vote.author,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_cannot_create_for_non_existent_question(
    api_client: APIClient, vote_data: VotePostData, user: User, decrypt_mock: MagicMock
) -> None:
    non_existent_answer_id = 667
    vote_data["answer"] = non_existent_answer_id
    decrypt_mock.return_value = non_existent_answer_id
    response = _create_vote(api_client, vote_data, user)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@mark.parametrize("param", ["answer", "election"])
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
    api_client: APIClient, vote_data: VotePostData, user: User, decrypt_mock: MagicMock
) -> None:
    response = _create_vote(api_client, vote_data, user)
    assert response.status_code == status.HTTP_403_FORBIDDEN
