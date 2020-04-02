from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from typing_extensions import TypedDict

from pytest import mark, fixture

from apollo.elections.models import Election, Question, Answer

AnswerPostData = TypedDict("AnswerPostData", {"text": str, "question": int})


@fixture
def answer_data(question: Question) -> AnswerPostData:
    return {"question": question.id, "text": "General Kenobi"}


def _create_answer(answer_data: AnswerPostData, user: User):
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    return api_client.post(
        reverse("elections:answer-list"), data=answer_data, format="json"
    )


@mark.django_db
def test_create_answer(answer_data: AnswerPostData, user: User) -> None:
    response = _create_answer(answer_data, user)
    assert response.status_code == status.HTTP_201_CREATED
    answer = Answer.objects.get(id=response.data["id"])
    assert all(
        (
            answer.question.id == answer_data["question"],
            answer.text == answer_data["text"],
        )
    )


@mark.django_db
def test_cannot_create_for_non_existent_question(
    answer_data: AnswerPostData, user: User
) -> None:
    answer_data["question"] = 667
    response = _create_answer(answer_data, user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "question" in response.data


@mark.django_db
@mark.parametrize("param", ["text", "question"])
def test_cannot_be_created_without_all_required_params(
    param: str, answer_data: AnswerPostData, user: User
) -> None:
    del answer_data[param]
    response = _create_answer(answer_data, user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert param in response.data


@mark.django_db
def test_question_cannot_be_added_by_non_authorized_users(
    answer_data: AnswerPostData, other_user: User
) -> None:
    old_answers_count = Answer.objects.count()
    response = _create_answer(answer_data, other_user)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Answer.objects.count() == old_answers_count
