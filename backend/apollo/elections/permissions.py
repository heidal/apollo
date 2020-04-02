from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from apollo.elections.models import Election, Question, Answer


class CanAddQuestion(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, question: Question
    ) -> bool:
        return self.has_permission(request, view)

    def has_permission(self, request: Request, view: APIView) -> bool:
        election_id = request.data.get("election")
        if election_id is None:
            # if we returned False then the error message wouldn't
            # be meaningful to the client (they would see that they
            # don't have permissions but the problem is that this field is missing)
            return True

        election = Election.objects.filter(id=election_id).first()
        if not election:
            return True

        return request.user == election.author


class CanAddAnswer(permissions.BasePermission):
    # FIXME: make this less-coupled to the logic inside the view/serializer
    def has_object_permission(
        self, request: Request, view: APIView, answer: Answer
    ) -> bool:
        return self.has_permission(request, view)

    def has_permission(self, request: Request, view: APIView) -> bool:
        question_id = request.data.get("question")
        if question_id is None:
            return True

        question = Question.objects.filter(id=question_id).first()
        if not question:
            return True

        return request.user == question.election.author
