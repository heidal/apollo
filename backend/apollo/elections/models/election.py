import hashlib
import secrets

from django.db import models
from django.db.models import Q
from django.utils.timezone import now
from django_fsm import FSMField, transition
from django_utils.choices import Choices, Choice
from nacl.public import PrivateKey
from nacl.encoding import Base64Encoder

from apollo.elections.models.vote import Vote
from apollo.elections.models.answer import Answer
from apollo.users.models import User
from apollo.elections.crypto import decrypt, CryptoError, SEED_BIT_SIZE, SEED_BYTE_SIZE


class Election(models.Model):
    class State(Choices):
        # note: choice must be a string to work with django_fsm
        CREATED = Choice("0", "CREATED")
        OPENED = Choice("1", "OPENED")
        CLOSED = Choice("2", "CLOSED")

    class Visibility(Choices):
        PRIVATE = Choice(0, "PRIVATE")
        PUBLIC = Choice(1, "PUBLIC")

    created_at = models.DateTimeField(auto_now_add=True)
    opened_at = models.DateTimeField(null=True)
    closed_at = models.DateTimeField(null=True)
    description = models.TextField()
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="elections")
    state = FSMField(default=State.CREATED)
    visibility = models.PositiveSmallIntegerField(
        choices=Visibility.choices, default=Visibility.PRIVATE
    )
    public_key = models.CharField(max_length=64, null=True, blank=False)
    secret_key = models.CharField(max_length=64, null=True, blank=False)
    seed = models.BinaryField(
        max_length=SEED_BYTE_SIZE, null=True, blank=False, editable=False
    )

    class Meta:
        ordering = ["created_at"]

    def can_be_opened(self) -> bool:
        """
        Check if the election fulfills the requirements to be opened.

        The list of requirements:
            * there is at least one question specified in the election
            * each question has at least one answer

        :return: True if the election can be opened, else False.
        """
        return (
            self.questions.all().exists()
            and not self.questions.filter(answers__isnull=True).exists()
        )

    def _open_votes(self):
        for vote in Vote.objects.filter(question__election=self):
            try:
                decrypted_answer_id = decrypt(self.secret_key, vote.answer_ciphertext)
                answer = Answer.objects.get(pk=decrypted_answer_id)
            except (CryptoError, Answer.DoesNotExist):
                pass
            else:
                if answer.question.election == self:
                    vote.answer = answer
                    vote.save()

    @transition(
        field=state,
        source=State.CREATED,
        target=State.OPENED,
        conditions=[can_be_opened],
    )
    def open(self) -> None:
        sk = PrivateKey.generate()
        self.secret_key = sk.encode(Base64Encoder()).decode("ascii")
        self.public_key = sk.public_key.encode(Base64Encoder()).decode("ascii")
        self.seed = secrets.randbits(SEED_BIT_SIZE).to_bytes(
            SEED_BYTE_SIZE, byteorder="big"
        )
        self.opened_at = now()

    @transition(field=state, source=State.OPENED, target=State.CLOSED)
    def close(self) -> None:
        self.closed_at = now()
        self._open_votes()

    @property
    def state_string(self) -> str:
        return str(Election.State.choices[self.state])

    @property
    def seed_hash(self) -> bytes:
        if self.seed is None:
            raise ValueError("Voter seed is None")
        hasher = hashlib.sha3_256()
        hasher.update(self.seed)
        return hasher.digest()

    def can_vote_in_election(self, user: User):
        return self.authorization_rules.authorized(user).exists()  # type: ignore


class VoterAuthorizationRuleQuerySet(models.QuerySet):
    @staticmethod
    def authorization_filter(user: User):
        return Q(type=VoterAuthorizationRule.Type.EXACT, value=user.email)

    def authorized(self, user: User):
        return self.filter(self.authorization_filter(user))

    def unauthorized(self, user: User):
        return self.exclude(self.authorization_filter(user))


class VoterAuthorizationRule(models.Model):
    class Type(Choices):
        EXACT = Choice(0, "EXACT")

    objects = VoterAuthorizationRuleQuerySet.as_manager()

    election = models.ForeignKey(
        Election, on_delete=models.CASCADE, related_name="authorization_rules"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(choices=Type.choices)
    value = models.CharField(max_length=100)

    def is_authorized(self, name: str) -> bool:
        if self.type == self.Type.EXACT:
            return self.value == name
        raise ValueError("VoterAuthorizationRule.Type invalid type")
