from typing import List

from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import SAFE_METHODS, BasePermission

from apollo.common.permissions import get_default_permission_classes
from apollo.elections.models import Answer, Election, Question, Vote
from apollo.elections.permissions import CanAddQuestion, CanAddAnswer
from apollo.elections.serializers import (
    AnswerSerializer,
    ElectionSerializer,
    QuestionSerializer,
    VoteSerializer,
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
    serializer_class = ElectionSerializer


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
