from typing import TypedDict

from apollo.users.models import User
from pytest import mark, fixture
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from apollo.elections.models import Answer, Vote

VotePostData = TypedDict("VotePostData", {"answer": int})


@fixture
def vote_data(answer: Answer) -> VotePostData:
    return {"answer": answer.id}


def _create_vote(vote_data: VotePostData, user: User) -> Response:
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    return api_client.post(
        reverse("elections:vote-list"), data=vote_data, format="json"
    )


@mark.django_db
def test_create_vote(vote_data: VotePostData, user: User) -> None:
    response = _create_vote(vote_data, user)
    assert response.status_code == status.HTTP_201_CREATED
    vote = Vote.objects.get(id=response.data["id"])
    assert all((vote.answer.id == vote_data["answer"], vote.author.id == user.id))


@mark.django_db
def test_create_vote_twice_on_the_same_thing(vote: Vote) -> None:
    response = _create_vote({"answer": vote.answer.id}, vote.author)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@mark.django_db
def test_cannot_create_for_non_existent_question(
    vote_data: VotePostData, user: User
) -> None:
    vote_data["answer"] = 667
    response = _create_vote(vote_data, user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "answer" in response.data


@mark.django_db
@mark.parametrize("param", ["answer"])
def test_cannot_be_created_without_all_required_params(
    param: str, vote_data: VotePostData, user: User
) -> None:
    del vote_data[param]
    response = _create_vote(vote_data, user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert param in response.data


@mark.django_db
def test_cannot_be_created_without_logging_in(vote_data: VotePostData) -> None:
    api_client = APIClient()
    response = api_client.post(
        reverse("elections:vote-list"), data=vote_data, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
