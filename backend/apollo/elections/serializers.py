from typing import Dict, List

from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from apollo.elections import permissions

import django_fsm
from rest_framework import serializers, exceptions
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator

from drf_writable_nested import serializers as nested
from apollo.elections.models import Answer, Election, Question, Vote
from apollo.elections.models.election import VoterAuthorizationRule
from apollo.common import serializers as apollo_serializers
from apollo.elections.crypto import decrypt, CryptoError


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "text", "question"]


class QuestionSerializer(serializers.ModelSerializer):
    election = serializers.PrimaryKeyRelatedField(queryset=Election.objects.all())
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "answers", "election", "question"]


class NestedAnswerSerializer(nested.WritableNestedModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "text"]
        read_only_fields = ["id"]


class NestedQuestionSerializer(nested.WritableNestedModelSerializer):
    answers = NestedAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "answers", "question"]
        read_only_fields = ["id"]


class VoteSerializer(
    apollo_serializers.AuthorizedSerializer, serializers.ModelSerializer
):
    def authorize(self, attrs):
        user = self.context["request"].user
        election = attrs["answer"].question.election
        if not permissions.can_vote_in_election(user, election):
            raise exceptions.PermissionDenied("VOTE_UNAUTHORIZED")

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

    def _decrypt_answer(self):
        election = get_object_or_404(Election, pk=self.initial_data.pop("election"))
        answer_id = decrypt(election.secret_key, self.initial_data["answer"])
        answer = get_object_or_404(Answer, pk=answer_id)

        if answer.question.election.id != election.id:
            raise ValidationError()

        return answer_id

    def is_valid(self, raise_exception):
        try:
            answer_id = self._decrypt_answer()
        except KeyError as e:
            if raise_exception:
                raise ValidationError(f"Missing parameter {e}")
        except (CryptoError, ValidationError):
            if raise_exception:
                raise ValidationError()

        self.initial_data["answer"] = answer_id
        return super().is_valid(raise_exception)


class VoterAuthorizationRuleSerializer(serializers.ModelSerializer):
    type = serializers.CharField()

    class Meta:
        model = VoterAuthorizationRule
        fields = ["type", "value"]

    def to_representation(self, instance: VoterAuthorizationRule) -> Dict:
        data = super().to_representation(instance)

        data["type"] = instance.get_type_display()
        return data

    def validate(self, attrs):
        rule_type = attrs.pop("type")
        try:
            rule_type = getattr(VoterAuthorizationRule.Type, rule_type)
        except AttributeError:
            raise serializers.ValidationError("INVALID_RULE_TYPE")
        else:
            attrs["type"] = rule_type
            return super().validate(attrs)


class ElectionSerializer(
    apollo_serializers.AuthorizedSerializer, nested.WritableNestedModelSerializer
):
    author = serializers.HiddenField(default=CurrentUserDefault())
    questions = NestedQuestionSerializer(many=True)
    is_owned = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    authorization_rules = VoterAuthorizationRuleSerializer(many=True, allow_null=True)
    permissions = serializers.SerializerMethodField()

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
            "authorization_rules",
            "permissions",
        ]
        read_only_fields = ["public_key"]

    def get_is_owned(self, election: Election) -> bool:
        return self.context["request"].user == election.author

    @staticmethod
    def get_state(election: Election) -> str:
        return election.state_string

    def authorize(self, attrs):
        if getattr(self.instance, "pk", None) is None:
            return  # it means that we're creating the election, so we must be the owner

        user = self.context["request"].user
        election = self.instance
        if not permissions.can_edit_election(user, election):
            raise exceptions.PermissionDenied("CANNOT_EDIT_ELECTION")

    def get_permissions(self, election: Election) -> List[str]:
        user = self.context["request"].user
        user_permissions = []

        if permissions.can_edit_election(user, election):
            user_permissions.append("CAN_EDIT")

        if permissions.can_vote_in_election(user, election):
            user_permissions.append("CAN_VOTE")

        return user_permissions


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
