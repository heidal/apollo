from rest_framework import serializers

from apollo.elections.models import Answer, Election, Question


class ElectionSerializer(serializers.HyperlinkedModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Question.objects.all()
    )

    class Meta:
        model = Election
        fields = ["description", "questions", "title"]
        depth = 3


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    answers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Answer.objects.all()
    )

    class Meta:
        model = Question
        fields = ["answers", "question"]


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ["text", "votes"]
