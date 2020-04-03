from pytest import mark, fixture
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from apollo.elections.models import Election
from django.contrib.auth.models import User
from django.http import HttpResponse
from typing_extensions import TypedDict


ElectionPostData = TypedDict("ElectionPostData", {"description": str, "title": str})


@fixture
def election_data() -> ElectionPostData:
    return {"description": "Election description", "title": "Election title"}


def _create_election(election_data: ElectionPostData, user: User) -> HttpResponse:
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    return api_client.post(
        reverse("elections:election-list"), data=election_data, format="json"
    )


@mark.django_db
def test_create_election(election_data: ElectionPostData) -> None:
    user = User.objects.create()
    response = _create_election(election_data, user)
    assert response.status_code == status.HTTP_201_CREATED
    election = Election.objects.last()
    assert election is not None
    assert all(
        (
            election.description == election_data["description"],
            election.title == election_data["title"],
        )
    )


@mark.django_db
def test_cannot_be_created_without_logging_in(election_data: ElectionPostData) -> None:
    api_client = APIClient()
    response = api_client.post(
        reverse("elections:election-list"), data=election_data, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
