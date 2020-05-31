from typing import Optional, Callable, List, Dict
from pytest_lazyfixture import lazy_fixture

from pytest import mark, fixture
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from apollo.elections import models as el_models
from apollo.elections.models import Election
from apollo.users.models import User
from typing_extensions import TypedDict

pytestmark = mark.django_db


ElectionPostData = TypedDict(
    "ElectionPostData",
    {
        "description": str,
        "title": str,
        "authorization_rules": List[str],
        "questions": List[Dict],
        "visibility": str,
    },
)


@fixture
def election_data() -> ElectionPostData:
    return {
        "description": "Election description",
        "title": "Election title",
        "authorization_rules": [],
        "questions": [],
        "visibility": "PUBLIC",
    }


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
def test_create_election(user: User, election_data: ElectionPostData) -> None:
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
    "_election", [lazy_fixture("opened_election"), lazy_fixture("closed_election")]
)
def test_cannot_be_edited_when_not_in_initial_state(
    _election: Election, election_data: ElectionPostData
) -> None:
    response = _edit_election(_election, election_data, _election.author)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@mark.parametrize(
    "_election", [lazy_fixture("election"), lazy_fixture("opened_election")]
)
def test_cannot_get_summary_of_not_closed_election(_election: Election) -> None:
    response = _get_election_summary(_election, _election.author)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_author_can_get_election_summary(closed_election: Election) -> None:
    response = _get_election_summary(closed_election, closed_election.author)
    assert response.status_code == status.HTTP_200_OK


def test_simple_user_can_get_election_summary(
    closed_election: Election, other_user: User
) -> None:
    response = _get_election_summary(closed_election, other_user)
    assert response.status_code == status.HTTP_200_OK


@mark.parametrize(
    "_election, transition_function",
    [
        (lazy_fixture("election"), _close_election),
        (lazy_fixture("opened_election"), _open_election),
        (lazy_fixture("closed_election"), _open_election),
        (lazy_fixture("closed_election"), _close_election),
    ],
)
def test_invalid_election_transitions(
    _election: Election,
    transition_function: Callable[[Election, User], Response],
    user: User,
) -> None:
    response = transition_function(_election, user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.data


def test_private_elections_are_not_listed(
    api_client: APIClient, election: Election, private_election: Election,
) -> None:
    response = api_client.get(reverse("elections:election-list"))
    election_ids = set(e["id"] for e in response.data["results"])
    assert private_election.id not in election_ids
    assert election.id in election_ids


class TestElectionList:
    PRIVATE = el_models.Election.Visibility.PRIVATE
    PUBLIC = el_models.Election.Visibility.PUBLIC

    @fixture(autouse=True)
    def elections_list(self, election_factory, eligible_voter_factory):
        elections = election_factory.create_batch(5, visibility=self.PUBLIC)
        elections.extend(election_factory.create_batch(5, visibility=self.PRIVATE))
        voters = [
            eligible_voter_factory(election=election) for election in elections[::2]
        ]
        return voters, elections

    @staticmethod
    def get_elections(api_client: APIClient, user: User = None):
        if user:
            api_client.force_authenticate(user=user)
        return api_client.get(reverse("elections:election-list"))

    def test_get_elections_list_unauthenticated(self, api_client: APIClient):
        response = self.get_elections(api_client)
        assert response.status_code == status.HTTP_200_OK
        results = [el["id"] for el in response.data["results"]]
        elections = el_models.Election.objects.filter(id__in=results)
        assert not elections.filter(visibility=self.PRIVATE).exists()

    def test_eligible_voters_can_see_private_elections(
        self, api_client: APIClient, elections_list
    ):
        voters, elections = elections_list
        user = voters[0]
        response = self.get_elections(api_client, user)
        assert response.status_code == status.HTTP_200_OK
        results = set(el["id"] for el in response.data["results"])

        available_elections_ids = [el.id for el in user.available_elections]
        assert all(el_id in results for el_id in available_elections_ids)

        unauthorized_private_elections = el_models.Election.objects.filter(
            visibility=self.PRIVATE
        ).exclude(id__in=available_elections_ids)
        assert not any(el.id in results for el in unauthorized_private_elections)


class TestBulletinBoard:
    @fixture(autouse=True)
    def election_with_voters(self, opened_election, vote_factory):
        for _ in range(5):
            vote_factory(question__election=opened_election)
        return opened_election

    @fixture
    def other_election_with_voters(self, election_factory, vote_factory):
        opened_election = election_factory(open=True)
        for _ in range(5):
            vote_factory(question__election=opened_election)
        return opened_election

    @staticmethod
    def get_bulletin_board(api_client: APIClient, election: Election):
        return api_client.get(reverse("elections:election-bulletin-board", kwargs={"pk": election.id}))

    def test_contains_voters(self, api_client: APIClient, opened_election: Election):
        voters = opened_election.voters.order_by("-created_at")

        response = self.get_bulletin_board(api_client, opened_election)
        assert response.status_code == status.HTTP_200_OK
        board = response.data
        assert board == [
            {
                "pseudonym": voter.pseudonym,
                "created_at": voter.created_at.isoformat().replace('+00:00', 'Z'),
                "vote_ciphertext_hash": voter.vote_ciphertext_hash
            }
            for voter in voters
        ]

    def test_other_elections_are_not_included(self, api_client: APIClient, opened_election, other_election_with_voters):
        voters = el_models.Voter.objects.exclude(election=opened_election)

        response = self.get_bulletin_board(api_client, opened_election)
        assert response.status_code == status.HTTP_200_OK
        board = response.data
        actual_pseudonyms = set(v["pseudonym"] for v in board)
        assert not any(voter.pseudonym in actual_pseudonyms for voter in voters)
