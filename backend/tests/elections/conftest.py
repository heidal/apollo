from typing import TypedDict
from pytest import fixture

from apollo.elections import models as el_models
from apollo.elections.models import Answer
from apollo.users.models import User


@fixture
def decrypt_mock(mocker, answer: Answer):
    mock = mocker.patch("apollo.elections.crypto.decrypt")
    mock.return_value = answer.id
    return mock


VotePostData = TypedDict("VotePostData", {"answer_ciphertext": str, "question": int})


@fixture
def vote_data(answer_in_opened_election: el_models.Answer) -> VotePostData:
    return {
        "answer_ciphertext": "hello there",
        "question": answer_in_opened_election.question.id,
    }


@fixture
def eligible_voter_factory(voter_authorization_rule_factory):
    def inner(user: User, election: el_models.Election):
        voter_authorization_rule_factory(
            election=election,
            value=user.email,
            type=el_models.VoterAuthorizationRule.Type.EXACT,
        )
        return user

    return inner


@fixture
def eligible_voter(eligible_voter_factory, user, opened_election):
    return eligible_voter_factory(user, opened_election)
