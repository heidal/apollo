import django_fsm
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
    is_owned = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Election
        fields = [
            "id",
            "description",
            "questions",
            "title",
            "author",
            "is_owned",
            "state",
            "public_key",
            "created_at",
        ]

    def get_is_owned(self, election: Election) -> bool:
        return self.context["request"].user == election.author

    @staticmethod
    def get_state(election: Election) -> str:
        return election.state_string


class ElectionTransitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = ["id", "state", "state_string"]

    STATE_CALLABLE_MAP = {
        Election.State.OPENED: Election.open,
        Election.State.CLOSED: Election.close,
    }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        transition_fn = ElectionTransitionSerializer.STATE_CALLABLE_MAP[attrs["state"]]
        try:
            transition_fn(self.instance)
        except django_fsm.TransitionNotAllowed:
            raise serializers.ValidationError("TRANSITION_NOT_ALLOWED")
        return attrs


class AnswerSummarySerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ["id", "votes", "text"]

    @staticmethod
    def get_votes(answer: Answer) -> int:
        return answer.votes.count()


class QuestionSummarySerializer(serializers.ModelSerializer):
    answers = AnswerSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "answers", "question"]


class ElectionSummarySerializer(serializers.ModelSerializer):
    questions = QuestionSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Election
        fields = ["id", "description", "title", "questions"]
