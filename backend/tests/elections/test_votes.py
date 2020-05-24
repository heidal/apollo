from typing import TypedDict

from apollo.users.models import User
from pytest import mark, fixture
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from apollo.elections.models import Answer, Vote, Election

VotePostData = TypedDict("VotePostData", {"answer_ciphertext": str, "question": int})

pytestmark = mark.django_db


@fixture
def vote_data(answer: Answer) -> VotePostData:
    return {"answer_ciphertext": "hello there", "question": answer.question.id}


@fixture
def eligible_voter(
    user_factory, voter_authorization_rule_factory, election: Election
) -> User:
    user = user_factory()
    voter_authorization_rule_factory(election=election, value=user.email)
    return user


def _create_vote(
    api_client: APIClient, vote_data: VotePostData, user: User
) -> Response:
    api_client.force_authenticate(user=user)
    return api_client.post(
        reverse("elections:vote-list"), data=vote_data, format="json"
    )


def test_create_vote(
    api_client: APIClient, vote_data: VotePostData, eligible_voter: User
) -> None:
    response = _create_vote(api_client, vote_data, eligible_voter)
    assert response.status_code == status.HTTP_201_CREATED
    vote = Vote.objects.get(id=response.data["id"])
    assert all(
        (
            vote.answer_ciphertext == vote_data["answer_ciphertext"],
            vote.author.id == eligible_voter.id,
            vote.question.id == vote_data["question"],
        )
    )


def test_create_vote_twice_on_the_same_question(
    api_client: APIClient, vote: Vote
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
