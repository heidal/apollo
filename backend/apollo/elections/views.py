from typing import List

from django.contrib.auth.models import AnonymousUser
from django.db import models as dj_models
from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response

from apollo.common.permissions import get_default_permission_classes
from apollo.elections import models
from apollo.elections import serializers
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
    queryset = models.Answer.objects.all()
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

    def get_queryset(self) -> dj_models.QuerySet:
        if isinstance(self.request.user, AnonymousUser):
            return models.Election.objects.filter(
                visibility=models.Election.Visibility.PUBLIC
            )

        return models.Election.objects.filter(
            Q(visibility=models.Election.Visibility.PUBLIC)
            | Q(author=self.request.user)
            | Q(
                dj_models.Exists(
                    models.VoterAuthorizationRule.objects.filter(  # TODO(adambudziak) reuse the logic
                        type=models.VoterAuthorizationRule.Type.EXACT,
                        value=self.request.user.email,
                        election=dj_models.OuterRef("pk"),
                    )
                )
            )
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
            self.get_object(), data={"state": models.Election.State.OPENED}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, url_path="close", methods=["post"])
    def close_election(self, request: Request, pk: int = None) -> Response:
        serializer = self.get_serializer(
            self.get_object(), data={"state": models.Election.State.CLOSED}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, url_name="summary", methods=["get"])
    def summary(self, request: Request, pk: int = None) -> Response:
        instance: models.Election = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        detail=True,
        url_path="bulletin-board",
        url_name="bulletin-board",
        methods=["get"],
    )
    def get_bulletin_board(self, request: Request, pk: int = None) -> Response:
        election = self.get_object()
        votes = models.Vote.objects.filter(question__election=election).order_by(
            "-created_at"
        )
        serializer = serializers.BulletinBoardVoteSerializer(votes, many=True)
        return Response(serializer.data)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
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
    queryset = models.Vote.objects.all()
    serializer_class = VoteSerializer
