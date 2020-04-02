from typing import List

from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, BasePermission

from apollo.common.permissions import get_default_permission_classes
from apollo.elections.models import Answer, Election, Question
from apollo.elections.permissions import CanAddQuestion, CanAddAnswer
from apollo.elections.serializers import (
    AnswerSerializer,
    ElectionSerializer,
    QuestionSerializer,
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

    def get_permissions(self) -> List[BasePermission]:
        permission_classes = get_default_permission_classes()
        if self.request.method not in SAFE_METHODS:
            permission_classes += [CanAddQuestion]

        return [perm() for perm in permission_classes]
