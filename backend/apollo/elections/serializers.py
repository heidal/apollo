from rest_framework import serializers

from apollo.elections.models import Answer, Election, Question


class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = ["description", "questions", "title"]
        depth = 3


class QuestionSerializer(serializers.ModelSerializer):
    election = serializers.PrimaryKeyRelatedField(queryset=Election.objects.all())

    class Meta:
        model = Question
        fields = ["answers", "election", "question"]


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = ["text", "votes", "question"]
        read_only_fields = ["votes"]
