from pytest_factoryboy import LazyFixture

from apollo.users.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from typing_extensions import TypedDict

from pytest import mark, fixture

from apollo.elections.models import Election, Question


QuestionPostData = TypedDict("QuestionPostData", {"question": str, "election": int})


@fixture
def question_data(election: Election) -> QuestionPostData:
    return {"election": election.id, "question": "Hello, there!"}


def _create_question(question_data: QuestionPostData, user: User):
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    return api_client.post(
        reverse("elections:question-list"), data=question_data, format="json"
    )


@mark.django_db
def test_create_question(question_data: QuestionPostData, user: User) -> None:
    response = _create_question(question_data, user)
    assert response.status_code == status.HTTP_201_CREATED
    question = Question.objects.get(id=response.data["id"])
    assert all(
        (
            question.election.id == question_data["election"],
            question.question == question_data["question"],
        )
    )


@mark.django_db
def test_cannot_create_for_non_existent_election(
    question_data: QuestionPostData, user: User
) -> None:
    question_data["election"] = 667
    response = _create_question(question_data, user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "election" in response.data


@mark.django_db
@mark.parametrize("param", ["question", "election"])
def test_cannot_be_created_without_all_required_params(
    param: str, question_data: QuestionPostData, user: User
) -> None:
    del question_data[param]
    response = _create_question(question_data, user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert param in response.data


@mark.django_db
def test_question_cannot_be_added_by_non_authorized_users(
    question_data: QuestionPostData, other_user: User
) -> None:
    old_questions_count = Question.objects.count()
    response = _create_question(question_data, other_user)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Question.objects.count() == old_questions_count


@mark.django_db
@mark.parametrize(
    "_election", [LazyFixture("opened_election"), LazyFixture("frozen_election")]
)
def test_cannot_add_questions_to_election_if_not_state_created(
    _election: Election, question_data: QuestionPostData, user: User
) -> None:
    response = _create_question(question_data, user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    print(response.data)
