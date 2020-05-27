from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from apollo.users.models import User
from tests.elections.conftest import VotePostData


def _create_vote(
    api_client: APIClient, vote_data: VotePostData, user: User
) -> Response:
    api_client.force_authenticate(user=user)
    return api_client.post(
        reverse("elections:vote-list"), data=vote_data, format="json"
    )
