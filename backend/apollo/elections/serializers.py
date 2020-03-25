from rest_framework import serializers

from apollo.elections.models import Answer, Election, Question


class ElectionSerializer(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Question.objects.all()
    )

    class Meta:
        model = Election
        fields = ["description", "questions", "title"]
        depth = 3


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Answer.objects.all()
    )

    class Meta:
        model = Question
        fields = ["answers", "question"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["text", "votes"]
