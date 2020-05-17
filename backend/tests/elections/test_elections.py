from typing import Optional, Callable

from pytest import mark, fixture, lazy_fixture
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from apollo.elections.models import Election
from apollo.users.models import User
from typing_extensions import TypedDict

pytestmark = mark.django_db


ElectionPostData = TypedDict("ElectionPostData", {"description": str, "title": str})


@fixture
def election_data() -> ElectionPostData:
    return {"description": "Election description", "title": "Election title"}


def _post_endpoint(url: str, data: Optional[dict], user: User) -> Response:
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    return api_client.post(url, data=data, format="json")


def _create_election(election_data: ElectionPostData, user: User) -> Response:
    return _post_endpoint(
        reverse("elections:election-list"), data=election_data, user=user
    )


def _open_election(election: Election, user: User) -> Response:
    return _post_endpoint(
        reverse("elections:election-open-election", kwargs={"pk": election.pk}),
        data=None,
        user=user,
    )


def _close_election(election: Election, user: User) -> Response:
    return _post_endpoint(
        reverse("elections:election-close-election", kwargs={"pk": election.pk}),
        data=None,
        user=user,
    )


def _edit_election(
    election: Election, election_data: ElectionPostData, user: User
) -> Response:
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    return api_client.patch(
        reverse("elections:election-detail", kwargs={"pk": election.pk}),
        data=election_data,
        format="json",
    )


def _get_election_summary(election: Election, user: User) -> Response:
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    return api_client.get(
        reverse("elections:election-summary", kwargs={"pk": election.pk})
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


def test_cannot_be_created_without_logging_in(election_data: ElectionPostData) -> None:
    api_client = APIClient()
    response = api_client.post(
        reverse("elections:election-list"), data=election_data, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@mark.parametrize(
    "_election", [lazy_fixture("opened_election"), lazy_fixture("frozen_election")]
)
def test_cannot_be_edited_when_not_in_initial_state(
    _election: Election, election_data: ElectionPostData
) -> None:
    response = _edit_election(_election, election_data, _election.author)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@mark.parametrize(
    "_election", [lazy_fixture("election"), lazy_fixture("opened_election")]
)
def test_cannot_get_summary_of_not_frozen_election(_election: Election) -> None:
    response = _get_election_summary(_election, _election.author)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_author_can_get_election_summary(frozen_election: Election) -> None:
    response = _get_election_summary(frozen_election, frozen_election.author)
    assert response.status_code == status.HTTP_200_OK


def test_simple_user_can_get_election_summary(
    frozen_election: Election, other_user: User
) -> None:
    response = _get_election_summary(frozen_election, other_user)
    assert response.status_code == status.HTTP_200_OK


@mark.parametrize(
    "_election, transition_function",
    [
        (lazy_fixture("election"), _close_election),
        (lazy_fixture("opened_election"), _open_election),
        (lazy_fixture("frozen_election"), _open_election),
        (lazy_fixture("frozen_election"), _close_election),
    ],
)
def test_invalid_election_transitions(
    _election: Election,
    transition_function: Callable[[Election, User], Response],
    user: User,
) -> None:
    response = transition_function(_election, user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.data
