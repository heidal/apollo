from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from apollo.elections.models import Answer, Election, Question


class ElectionSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Election
        fields = ["id", "description", "questions", "title", "author"]
        depth = 3


class QuestionSerializer(serializers.ModelSerializer):
    election = serializers.PrimaryKeyRelatedField(queryset=Election.objects.all())

    class Meta:
        model = Question
        fields = ["id", "answers", "election", "question"]
        read_only_fields = ["answers"]


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = ["id", "text", "votes", "question"]
        read_only_fields = ["votes"]
