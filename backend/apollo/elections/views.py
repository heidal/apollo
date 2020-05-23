from typing import List

from django.contrib.auth.models import AnonymousUser
from django.db.models import QuerySet
from django.db.models.expressions import Exists
from django.db.models.query_utils import Q
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response

from apollo.common.permissions import get_default_permission_classes
from apollo.elections.models import Answer, Election, Question, Vote
from apollo.elections.models.election import VoterAuthorizationRule
from apollo.elections.permissions import (
    CanAddQuestion,
    CanAddAnswer,
    IsElectionMutable,
    IsElectionClosed,
    IsElectionAuthor,
)
from apollo.elections.serializers import (
    AnswerSerializer,
    ElectionSerializer,
    QuestionSerializer,
    VoteSerializer,
    ElectionSummarySerializer,
    ElectionTransitionSerializer,
)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get_permissions(self) -> List[BasePermission]:
        permission_classes = get_default_permission_classes()
        if self.request.method not in SAFE_METHODS:
            permission_classes += [CanAddAnswer]

        return [perm() for perm in permission_classes]


class ElectionViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["author"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self) -> QuerySet:
        if isinstance(self.request.user, AnonymousUser):
            return Election.objects.filter(visibility=Election.Visibility.PUBLIC)

        return Election.objects.filter(
            Q(visibility=Election.Visibility.PUBLIC)
            | Q(author=self.request.user)
            | Q(Exists(
                VoterAuthorizationRule.objects.filter(
                    type=VoterAuthorizationRule.Type.EXACT,
                    value=self.request.user.email,
                )
            ))
        )

    def get_permissions(self) -> List[BasePermission]:
        permission_classes = get_default_permission_classes()
        if self.action in ("update", "partial_update", "delete"):
            permission_classes += [IsElectionAuthor & IsElectionMutable]  # type: ignore
        elif self.action in ("summary",):
            permission_classes += [IsElectionClosed]

        return [perm() for perm in permission_classes]

    def get_serializer_class(self):
        if self.action == "summary":
            return ElectionSummarySerializer
        elif self.action in ("open_election", "close_election"):
            return ElectionTransitionSerializer
        return ElectionSerializer

    @action(detail=True, url_path="open", methods=["post"])
    def open_election(self, request: Request, pk: int = None) -> Response:
        serializer = self.get_serializer(
            self.get_object(), data={"state": Election.State.OPENED}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, url_path="close", methods=["post"])
    def close_election(self, request: Request, pk: int = None) -> Response:
        serializer = self.get_serializer(
            self.get_object(), data={"state": Election.State.CLOSED}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, url_name="summary", methods=["get"])
    def summary(self, request: Request, pk: int = None) -> Response:
        instance: Election = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["election"]
    ordering_fields = ["created_at"]
    ordering = ["created_at"]

    def get_permissions(self) -> List[BasePermission]:
        permission_classes = get_default_permission_classes()
        if self.request.method not in SAFE_METHODS:
            permission_classes += [CanAddQuestion]

        return [perm() for perm in permission_classes]


class VoteViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
