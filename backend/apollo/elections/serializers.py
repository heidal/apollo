from rest_framework import serializers

from apollo.elections.models import Answer, Election, Question


class ElectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Election
        fields = ["description", "questions", "title"]
        depth = 3


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ["answers", "question"]


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ["text", "votes"]
