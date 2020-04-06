from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator

from apollo.elections.models import Answer, Election, Question, Vote


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = ["id", "text", "question"]


class QuestionSerializer(serializers.ModelSerializer):
    election = serializers.PrimaryKeyRelatedField(queryset=Election.objects.all())
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "answers", "election", "question"]


class VoteSerializer(serializers.ModelSerializer):
    answer = serializers.PrimaryKeyRelatedField(queryset=Answer.objects.all())
    author = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Vote
        fields = ["id", "answer", "author"]
        read_only_fields = ["id"]
        validators = [
            UniqueTogetherValidator(
                queryset=Vote.objects.all(), fields=["author", "answer"]
            )
        ]


class ElectionSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=CurrentUserDefault())
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Election
        fields = ["id", "description", "questions", "title", "author"]
