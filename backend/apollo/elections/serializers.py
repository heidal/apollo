import base64
from typing import Dict, List

import django_fsm
from django.contrib.auth.models import AnonymousUser
from drf_writable_nested import serializers as nested
from rest_framework import serializers, exceptions
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator

import apollo.elections.models.vote
from apollo.common import serializers as apollo_serializers
from apollo.elections import permissions
from apollo.elections.models import Answer, Election, Question, Vote
from apollo.elections import models as el_models

from apollo.elections.models.election import VoterAuthorizationRule


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
        election = attrs["question"].election
        if not election.can_vote_in_election(user):
            raise exceptions.PermissionDenied("VOTE_UNAUTHORIZED")

    author = serializers.HiddenField(default=CurrentUserDefault())
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.filter(election__state=Election.State.OPENED)
    )

    class Meta:
        model = Vote
        fields = ["id", "answer_ciphertext", "author", "question"]
        read_only_fields = ["id"]
        validators = [
            UniqueTogetherValidator(
                queryset=Vote.objects.all(), fields=["author", "question"]
            )
        ]


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
            raise serializers.ValidationError({"type": "INVALID_RULE_TYPE"})

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
    visibility = serializers.CharField()
    did_vote = serializers.SerializerMethodField()

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
            "visibility",
            "did_vote",
        ]
        read_only_fields = ["public_key"]

    @staticmethod
    def validate_visibility(visibility: str) -> int:
        return getattr(Election.Visibility, visibility)

    def get_is_owned(self, election: Election) -> bool:
        user = self.context["request"].user
        if isinstance(user, AnonymousUser):
            return False
        return self.context["request"].user == election.author

    def get_did_vote(self, election: Election) -> bool:
        user = self.context["request"].user
        if isinstance(user, AnonymousUser):
            return False
        return el_models.Voter.objects.filter(user=user, election=election).exists()

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
        if not user.is_authenticated:
            return []

        user_permissions = []

        if permissions.can_edit_election(user, election):
            user_permissions.append("CAN_EDIT")

        if election.can_vote_in_election(user):
            user_permissions.append("CAN_VOTE")

        return user_permissions

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["visibility"] = Election.Visibility.choices[int(data["visibility"])].label
        return data


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


class ElectionUserMeSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    election = serializers.PrimaryKeyRelatedField(
        queryset=el_models.Election.objects.all()
    )

    def validate(self, attrs):
        voter = el_models.Voter.objects.filter(
            user=attrs["user"], election=attrs["election"]
        ).first()
        if not voter:
            raise serializers.ValidationError("VOTER_DOES_NOT_EXIST")

        attrs["user_seed_hash"] = base64.b64encode(voter.seed_hash)

        return super().validate(attrs)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user_seed_hash"] = self.validated_data["user_seed_hash"]
        return data


class BulletinBoardVoteSerializer(serializers.ModelSerializer):
    pseudonym = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    class Meta:
        model = el_models.Vote
        fields = ["pseudonym", "created_at", "question", "message"]
        read_only_fields = fields

    @staticmethod
    def get_voter(vote: el_models.Vote) -> el_models.Voter:
        election = vote.question.election
        return vote.author.voters.get(election=election)

    def get_pseudonym(self, vote: el_models.Vote):
        return self.get_voter(vote).pseudonym

    @staticmethod
    def get_message(vote: el_models.Vote):
        return vote.answer_ciphertext


class AnswerSummarySerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ["id", "votes", "text"]
        read_only_fields = fields

    @staticmethod
    def get_votes(answer: Answer) -> int:
        return answer.votes.count()


class QuestionSummarySerializer(serializers.ModelSerializer):
    answers = AnswerSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "answers", "question"]
        read_only_fields = fields


class ElectionSummarySerializer(serializers.ModelSerializer):
    questions = QuestionSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Election
        fields = ["id", "description", "title", "questions"]
        read_only_fields = fields
