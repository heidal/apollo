from typing import List

from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
import nacl

from apollo.common.permissions import get_default_permission_classes
from apollo.elections.models import Answer, Election, Question, Vote
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
    queryset = Election.objects.all()

    def get_permissions(self) -> List[BasePermission]:
        permission_classes = get_default_permission_classes()
        if self.action in ("update", "partial_update", "delete"):
            permission_classes += [IsElectionAuthor & IsElectionMutable]  # type: ignore
        elif self.action in ("summary",):
            permission_classes += [IsElectionClosed]  # type: ignore

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


class VoteViewSet(viewsets.GenericViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request):
        print(request.data)
        try:
            answer_id_ciphertext = request.data["answer"]
            ephemeral_pk = request.data["pk"]
            election_id = request.data["election"]
        except KeyError as e:
            return Response(f"Key {e} not found", status=status.HTTP_400_BAD_REQUEST)

        election = get_object_or_404(Election, pk=election_id)

        try:
            encoder = nacl.encoding.Base64Encoder()

            election_sk = nacl.public.PrivateKey(
                election.secret_key.encode("ascii"),
                encoder
            )

            ephemeral_pk = nacl.public.PublicKey(
                ephemeral_pk.encode("ascii"),
                encoder
            )

            box = nacl.public.Box(election_sk, ephemeral_pk)

            answer_id = box.decrypt(answer_id_ciphertext.encode("ascii")).decode("ascii")
        except nacl.exceptions.CryptoError as e:
            return Response("Sth went wrong {e}", status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={"answer": answer_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
