from django.views import View
from rest_framework import permissions
from rest_framework.request import Request

from apollo.elections.models import Election, Question, Answer
from apollo.users.models import User


def can_edit_election(user: User, election: Election) -> bool:
    return election.state == Election.State.CREATED and user == election.author


class IsElectionClosed(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, election: Election
    ) -> bool:
        return election.state == Election.State.CLOSED


class IsElectionAuthor(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, election: Election
    ) -> bool:
        return election.author == request.user


class IsElectionMutable(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, election: Election
    ) -> bool:
        return election.state == Election.State.CREATED


class CanAddQuestion(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, question: Question
    ) -> bool:
        return self.has_permission(request, view)

    def has_permission(self, request: Request, view: View) -> bool:
        election_id = request.data.get("election")
        if election_id is None:
            # if we returned False then the error message wouldn't
            # be meaningful to the client (they would see that they
            # don't have permissions but the problem is that this field is missing)
            return True

        election = Election.objects.filter(id=election_id).first()
        if not election:
            return True

        return can_edit_election(request.user, election)


class CanAddAnswer(permissions.BasePermission):
    # FIXME: make this less-coupled to the logic inside the view/serializer
    # Django permissions are not really that robust and in many cases it's hard
    # to build them in such a way that they can be used in multiple views and still
    # be maintainable.

    # In case of this permission we rely on the consistency between this class and the
    # serializer that performs validation of the request. If the request doesn't have
    # a `question` specified, then we return `True` to fallback to the validation of
    # the serializer that is performed later. However, if the serializer expects
    # a field called `question_id` instead of `question` (because we changed it there and forgot
    # to align it here) then this permission will allow any request to pass.

    # On the other hand, if we just return False when the request is invalid, then
    # the client will get an error code that is inappropriate for the reason of
    # the rejection (403 instead of 400).
    def has_object_permission(
        self, request: Request, view: View, answer: Answer
    ) -> bool:
        return self.has_permission(request, view)

    def has_permission(self, request: Request, view: View) -> bool:
        question_id = request.data.get("question")
        if question_id is None:
            return True

        question = Question.objects.filter(id=question_id).first()
        if not question:
            return True

        return can_edit_election(request.user, question.election)


def can_vote_in_election(user: User, election: Election) -> bool:
    return any(
        rule.is_authorized(user.email) for rule in election.authorization_rules.all()
    )
