from rest_framework import viewsets

from apollo.elections.models import Answer, Election, Question
from apollo.elections.serializers import (
    AnswerSerializer,
    ElectionSerializer,
    QuestionSerializer,
)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
